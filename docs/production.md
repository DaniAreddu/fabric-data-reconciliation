# From the example to a production flow

The example is built to be read in one sitting: nine rows, one review, every decision visible. The protections it demonstrates still apply at scale (namespaced source keys, preserved originals, rule order, scoped reviews, whole-group checks, field provenance). The mechanisms behind several of them do not scale or are deliberately simplified. This page lists what would have to change.

## Grouping runs on the driver

`consolidate()` collects all current rows and candidate pairs to the Spark driver and groups them with a Python union-find. For nine rows that keeps the group checks easy to read. With real volumes it runs out of memory long before it finds the right answer, and simply collecting more rows does not solve identity.

Production needs distributed grouping (connected components over the accepted edges) that applies the same checks: no group may contain two different reliable IDs or a recorded rejection, and an unresolved singleton must not slip into a supported group.

## Candidates are recomputed on the whole snapshot

The notebook ingests B002 incrementally, one changed row, but then rebuilds Silver, candidates and Gold from the full current snapshot. That is incremental ingestion, not incremental matching. A production flow has to:

- find the blocks and groups affected by new, changed or deleted rows and reprocess only those;
- define what a deleted source row means for the published company;
- handle late-arriving changes and ties between versions explicitly. The example orders by source update time, then batch; a later load time alone does not mean a newer source value;
- monitor candidate counts per block, since one very common postcode or name prefix can produce a block that is too large (skew).

## Customer IDs are derived, not registered

`CUS-a60635aa3160` is a hash of `business:DEMO-001`, or of the first source key when a group has no reliable ID. That keeps Alfa stable through the B002 address change, and it is the only change the example demonstrates. It fails as soon as identity itself changes:

- a reliable ID is added to a group that had none, so the anchor changes from a source key to the business ID;
- an ID is corrected, and every derived ID changes with it;
- two companies turn out to be one (merge) or one turns out to be two (split).

Production needs a persistent identity registry: a table that issues customer IDs once and stores the history of entities, source mappings, merges, splits and corrections, so that consumers can follow an old ID to its current entity instead of silently losing it.

## Reviews need a lifecycle

The example stores one current decision per pair in a CSV and rechecks it with a fingerprint and rule version. A production review process also needs:

- a way to flag decisions whose evidence has been withdrawn or corrected, even when the record fields are unchanged; the reference does not implement this;
- versioned decisions, so that the decision in force on a given date can be reconstructed;
- owners and service targets for the review queue, and permissions on sensitive evidence;
- correction and split workflows that undo an approved link and everything published from it.

## Evidence must be calibrated

The weights (60/25/15), the threshold (70) and the blocking rule are illustrative. Before trusting them:

- label a sample of pairs that the rules did not help choose, including difficult negatives such as two companies sharing an office;
- measure false links (different entities joined), missed links (one entity left split) and blocking coverage (true pairs that never reached comparison);
- keep `UNKNOWN` labels out of the measurement and track how many there are;
- decide which error costs more for each use. A wrong invoice address and a split support history are different problems.

The five labelled pairs in this repository are a conformance check of the example, not an accuracy estimate.

## Normalisation and reliability are domain work

The normaliser lower-cases text, strips punctuation and expands `St.` to `Street`. Real addresses need a parser that knows the country's formats, distinguishes address roles (billing, delivery, site) and keeps the original. Company identifiers need a reliability assessment per source: a well-formed ID can still be wrong.

## Location data

If a production flow uses coordinates, as the Messina platform did with PostGIS, treat proximity as a clue that narrows the search, never as proof of identity. Check units: with `geometry` in WGS84, distances are in degrees; with `geography`, in metres.

## Publication and consumers

- Create a semantic model explicitly from the Gold tables intended for analytics. Fabric no longer creates default semantic models automatically for new lakehouses.
- Applications that need customer lookups need a separately designed backend or API.
- Keep each medallion layer in its own Lakehouse with its own permissions. Table prefixes in one Lakehouse are not access control.
- Decide what consumers see for held records: here `PORTAL:P902` is simply absent from Gold, and listed in `recon_demo_held_records`.

## What the example does not include

No live connectors to CRM, ERP or portal APIs, no pipeline definition, no review application, no identity registry, no deletes, no monitoring. The Messina loop's confirmation of applied updates, safe retry and idempotency are proposed patterns, not implemented here.
