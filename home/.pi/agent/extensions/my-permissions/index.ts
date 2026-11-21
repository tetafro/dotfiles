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
    outcome: "allow" | "deny" | "ask";
    reason: string;
};

// permissions is the extension's entry point. Pi calls it on load. It registers
// the allow/deny/ask gate for tool calls.
export default function permissions(pi: ExtensionAPI) {
    const configPath = join(process.env.PI_CODING_AGENT_DIR || join(homedir(), ".pi", "agent"), "my-permissions.jsonc");
    pi.on("tool_call", async (event, ctx) => {
        try {
            const decision = await authorize({
                toolName: event.toolName,
                input: event.input,
                cwd: ctx.cwd,
                parentToolCallId: event.parentToolCallId,
            }, ctx, configPath);

            if (decision.outcome !== "allow") {
                return { block: true, reason: decision.reason };
            }
        } catch {
            // Never let a failed permission check silently execute the action.
            return { block: true, reason: "Permission check failed" };
        }
    });
}

// authorize resolves an action to a final allow/deny verdict.
export async function authorize(action: Action, ctx: ExtensionContext): Promise<Decision> {
    const staticDecision = checkStaticRules(action);
    if (staticDecision.outcome !== "ask") {
        return staticDecision;
    }

    const allowed = await askUser(action, staticDecision, ctx);
    return {
        outcome: allowed ? "allow" : "deny",
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
export function checkStaticRules(action: Action): Decision {
    const directoryDecision = checkDirectoryRules(action);
    if (directoryDecision?.outcome === "deny") {
        return directoryDecision;
    }

    let decision: Decision | undefined;
    if (action.toolName === "bash") {
        decision = checkBashRules(action);
    }
    if (decision === undefined) {
        decision = checkToolRules(action);
    }
    if (decision.outcome === "deny") {
        return decision;
    }

    // A directory `ask` can override an `allow`
    if (directoryDecision?.outcome === "ask") {
        return directoryDecision;
    }
    return decision;
}

// checkToolRules checks rules for registered tools (including MCP).
export function checkToolRules(_action: Action): Decision {
    return { outcome: "allow", reason: "No matching tool rule" };
}

// checkBashRules determines access to a shell command as a whole, including
// chained or piped commands.
export function checkBashRules(_action: Action): Decision | undefined {
    return undefined;
}

// checkDirectoryRules applies independent checks to file-tool access outside
// the working directory.
export function checkDirectoryRules(_action: Action): Decision | undefined {
    return undefined;
}
