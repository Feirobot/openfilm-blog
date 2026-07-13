# OpenFilm Auto Blog Workflow

## Fixed tool path (2026-07-14)

- `.pipeline/trigger-next.sh`: checks the stage, repairs trigger bindings, and starts only the next stage.
- `.pipeline/publish-media.js`: converts sources to WebP with sharp, uploads directly to R2, and verifies public objects without printing credentials.
- `.pipeline/insert-blog-images.py`: inserts bilingual images idempotently and advances the state to `images_generated`.
- `.pipeline/publish-blog.py`: performs the build, scoped staging, standard Git push, deployment checks, and final state commit.

`publish-blog.py` supports resuming after the bilingual article commit: when both articles are already `draft: false`, clean, and were committed together, it reuses that content commit and continues from push/deployment verification.

Stage tool-call budgets are 18, 10, 20, and 6. A fixed helper failure must stop the stage; agents may not explore an alternative toolchain.

Reference sections use `## 参考资料` / `## References` followed by 3-7 unordered Markdown links in the exact form `- [descriptive title](https://direct-source)`.

This workflow is implemented as one scheduled QoderWake automation plus three
API-triggered automations coordinated by
`/root/AIwork/openfilm-blog/.pipeline/status.json`.

Stages and triggers:

1. Scheduled: `idle` or completed previous run -> `draft_created` by `胶片编辑`
   - Waker: `221d20684be7`
   - Automation: `tr_ad39249772024519`
   - Cron: `0 4 * * *`, timezone `Asia/Shanghai`
2. API/run-now: `draft_created` -> `translated` by `启航`
   - Waker: `57517720e12a`
   - Automation: `tr_516ea4db27cb47d7`
3. API/run-now: `translated` -> `images_generated` by `画师`
   - Waker: `d9b25b78e908`
   - Automation: `tr_0e49b354967e4f3f`
4. API/run-now: `images_generated` -> `published` by `启航`
   - Waker: `57517720e12a`
   - Automation: `tr_7a6182a67db84957`

Only the first automation is scheduled. Later stages must not run on cron; they
are triggered by the previous stage after the status file is updated.

Active-run lock:

- `workflow_state: "running"` means a round is in progress.
- `workflow_run_id` identifies the active round.
- The first automation must not start a new round unless `workflow_state` is
  absent, `idle`, `completed`, `failed`, or the last stage is `published`.
- Each downstream automation must verify both `workflow_run_id` and `stage`.

Topic deduplication:

- Before drafting, the first automation must inspect existing `*-zh.mdx` posts,
  including slug, title, description, and tags.
- New topics should avoid already-covered broad themes. Nearby subjects are
  acceptable only when the angle is clearly narrower or materially different.
- The draft stage history entry should mention the closest old posts checked
  and why the new topic is not a repeat.

Runtime notes:

- All active automations are enabled. Later stages are API-kind automations with
  no cron schedule, so `run-now` can invoke them without timer overlap.
- The active first automation is not bound to `proj_30acfc01`; it uses the
  source workspace directly to avoid project onboarding/worktree errors.
- Server runtime has Node.js `v22.16.0` and npm `10.9.2` on PATH.
- GitHub HTTPS credentials are configured for normal `git push origin main`.
- `repair-qoderwake-triggers.py` is run by a server timer. It restores all four
  automations to `workspaceSource`, removes stale project binding fields, and
  re-enables accidentally disabled triggers.
- Run the repair script immediately after every `qoderwake-cn automation update`.
- External commands in stage prompts have explicit time limits. Timeouts must be
  recorded in status history and must not leave a run waiting indefinitely.
