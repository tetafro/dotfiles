import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { isAbsolute, join, matchesGlob, relative, resolve, sep } from "node:path";
import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";

// Action is a proposed tool invocation and its relevant execution context.
export type Action = {
    toolName: string;
    input: Record<string, unknown>;
    cwd: string;
    parentToolCallId?: string;
};

// Decision is a permission verdict on a proposed action.
export type Decision = {
    action: "allow" | "deny" | "ask";
    reason: string;
};

// Config holds the permission rules.
type Config = {
    directories: DirectoryRule[];
    tools: ToolRule[];
};

// ToolRule sets the permission for a tool name.
type ToolRule = {
    name: string;
    action: "allow" | "ask";
};

// DirectoryRule sets the permission for a directory and its descendants.
type DirectoryRule = {
    path: string;
    action: "read" | "write" | "ask";
};

// loadConfig reads and validates the permission config.
function loadConfig(path: string): Config {
    const config: Config = { directories: [], tools: [] };

    const data = JSON.parse(readFileSync(path, "utf8"));
    if (!isObject(data)) {
        throw new Error("Expected a config object");
    }

    // Directories
    if (!isObject(data.directories)) {
        throw new Error("Expected a directories object");
    }
    for (const [path, action] of Object.entries(data.directories)) {
        if (!["read", "write", "ask"].includes(action)) {
            throw new Error(`Unexpected action in directory rules: '${action}'`);
        }
        if (!isAbsolute(path)) {
            throw new Error(`Directory rule path is not absolute: '${path}'`);
        }
        config.directories.push({ path, action });
    }

    // Tools
    if (!isObject(data.tools)) {
        throw new Error("Expected a tools object");
    }
    for (const [name, action] of Object.entries(data.tools)) {
        if (!["allow", "ask"].includes(action)) {
            throw new Error(`Unexpected action in tool rules: '${action}'`);
        }
        config.tools.push({ name, action });
    }

    return config;
}

// permissions is the extension's entry point. Pi calls it on load. It registers
// the allow/deny/ask gate for tool calls.
export default function permissions(pi: ExtensionAPI) {
    const configPath = join(process.env.PI_CODING_AGENT_DIR || join(homedir(), ".pi", "agent"), "my-permissions.json");
    let config: Config | undefined;
    try {
        config = loadConfig(configPath);
    } catch (error) {
        console.error(`my-permissions: ${error}`);
    }

    pi.on("tool_call", async (event, ctx) => {
        try {
            const decision = await authorize({
                toolName: event.toolName,
                input: event.input,
                cwd: ctx.cwd,
                parentToolCallId: event.parentToolCallId,
            }, ctx, config);

            if (decision.action !== "allow") {
                return { block: true, reason: decision.reason };
            }
        } catch {
            // Never let a failed permission check silently execute the action.
            return { block: true, reason: "Permission check failed" };
        }
    });
}

// authorize resolves an action to a final allow/deny verdict.
export async function authorize(action: Action, ctx: ExtensionContext, config: Config | undefined): Promise<Decision> {
    const staticDecision = checkStaticRules(action, config);
    if (staticDecision.action !== "ask") {
        return staticDecision;
    }

    const allowed = await askUser(action, staticDecision, ctx);
    return {
        action: allowed ? "allow" : "deny",
        reason: allowed ? "Approved by user" : staticDecision.reason,
    };
}

// askUser requests one-time human approval if static rules didn't help.
export async function askUser(
    action: Action,
    decision: Decision,
    ctx: ExtensionContext,
): Promise<boolean> {
    if (!ctx.hasUI || ctx.signal?.aborted) {
        return false;
    }
    const args = JSON.stringify(action.input, null, 2); // pretty-print
    const approved = await ctx.ui.confirm(
        "Allow " + action.toolName + "?",
        decision.reason + "\n" + action.cwd + "\n" + args,
    );
    return approved && !ctx.signal?.aborted;
}

// checkStaticRules produces the combined static verdict based on the rules.
export function checkStaticRules(action: Action, config: Config | undefined): Decision {
    const directoryDecision = checkDirectoryRules(action, config?.directories);

    let decision: Decision | undefined;
    if (action.toolName === "bash") {
        decision = checkBashRules(action);
    }
    if (decision === undefined) {
        decision = checkToolRules(action, config?.tools);
    }
    if (directoryDecision.action === "ask") {
        return directoryDecision;
    }
    return decision;
}

// checkToolRules checks rules for registered tools (including MCP).
export function checkToolRules(action: Action, rules: ToolRule[]): Decision {
    const rule = rules?.find((rule) => matchesGlob(action.toolName, rule.name));
    if (rule === undefined) {
        return { action: "ask", reason: "No matching tool rule" };
    }
    return { action: rule.action, reason: `Tool rule: ${rule.name} (${rule.action})` };
}

// checkBashRules determines access to a shell command as a whole, including
// chained or piped commands.
export function checkBashRules(_action: Action): Decision | undefined {
    return undefined;
}

// checkDirectoryRules checks the requested path.
export function checkDirectoryRules(action: Action, rules: DirectoryRule[]): Decision {
    // Check only file tools here, bash filesystem access is controlled by bubblewrap
    if (!["read", "write", "edit", "ls", "find", "grep"].includes(action.toolName)) {
        return { action: "allow", reason: "Not a file tool" };
    }

    const input = action.input.path ?? ".";
    if (typeof input !== "string" || !input) {
        return { action: "ask", reason: "Invalid file path" };
    }

    // Build the full path
    let path = input.replace(/^@/, "");
    if (path === "~" || path.startsWith("~/")) {
        path = homedir() + path.slice(1);
    }
    const absolute = resolve(action.cwd, path);

    // TODO: Resolve symlinks before matching directory rules.
    const fromCwd = relative(action.cwd, absolute);
    if (fromCwd !== ".." && !fromCwd.startsWith(".." + sep) && !isAbsolute(fromCwd)) {
        return { action: "allow", reason: "Inside the working directory" };
    }

    let decision: Decision = {
        action: "ask",
        reason: "No matching directory rule",
    };
    if (rules === undefined) {
        return decision;
    }
    const modifies = action.toolName === "write" || action.toolName === "edit";
    for (const rule of rules) {
        // Check if the path is outside of the rule's directory (ignore names starting with "..")
        if (relative(rule.path, absolute).startsWith("..")) {
            continue;
        }
        decision = {
            action: "ask",
            reason: `Directory rule: ${rule.path} (${rule.action})`,
        };
        if (rule.action === "read" && !modifies) {
            decision.action = "allow";
        }
        if (rule.action === "write") {
            decision.action = "allow";
        }
        if (decision.action === "ask") {
            return decision;
        }
    }
    return decision;
}

// isObject reports whether a value is an object.
function isObject(value: any): boolean {
    return value !== undefined &&
        value !== null &&
        typeof value === "object" &&
        !Array.isArray(value);
}
