# Palantir Federal Award Data: Method, Results, and Limits

Retrieved October 31, 2026 from the public USAspending.gov programming interface.

## What was queried

Contract awards (award types A to D) to three recipients: Palantir Technologies Inc., Palantir USA Inc., and Palantir USG Inc. Other recipients with similar names (for example Palantir.net Inc.) were excluded. Figures are federal action obligations by action date, grouped by fiscal year (October to September). They include modifications and any deobligations. They are not disbursements. Subcontracts are not included.

## Results

Annual obligations are in palantir_obligations_by_fy.csv. Fiscal 2014 to 2024 rose from $75 million to $541 million, fiscal 2025 was $1,021 million and fiscal 2026 $1,992 million (possibly incomplete or revised). Cumulative obligations through fiscal 2024 were about $2.58 billion, matching the $2.5 billion in Durán, and fiscal 2024 was $541 million against his $531 million.

By administration, with months assigned approximately and January assigned to the outgoing administration, annual averages were about $52 million (Obama), $179 million (first Trump), $419 million (Biden), and about $1.67 billion annualized over the 20 months of the second Trump administration so far.

The 120 largest awards (palantir_top120_awards_competition.csv) cover about 89 percent of the obligations in the set. By value, about 50 percent carry a not-competed, only-one-source coding and about 46 percent carry full and open competition. The not-competed share by era of award start was about 53 percent (Obama), 15 percent (first Trump), 55 percent (Biden) and 60 percent (second Trump so far).

The enterprise agreement W519TC25D0039 is a single-award indefinite-delivery/indefinite-quantity contract signed July 31, 2025, described as a consolidated enterprise agreement for Palantir USG Inc's commercial solutions, with a ceiling of $10 billion, no obligations on the vehicle itself, and a not-competed, only-one-source, one-offer coding. It has 40 orders (ea_W519TC25D0039_orders.csv) with $1,226 million obligated, about 12 percent of the ceiling, of which $54.7 million fell in fiscal 2025 and $1,171.7 million in fiscal 2026. Reported outlays are $11.5 million, from a different reporting stream with its own timing and coverage, so they should not be read as delayed execution. The largest order, $637.6 million for a Defense Department Maven Smart System task order, is 52 percent of obligations under the agreement. The agreement carried about 59 percent of Palantir's fiscal 2026 obligations, and the other $820 million still exceeded all of fiscal 2024.

## Sensitivity of the competition figures

Counting awards coded not competed under simplified acquisition procedures as well, 53 percent of the value of the 120 largest awards is not competed, against 34 percent by count and 57 percent for the 60 largest by value. Excluding the 15 orders under the enterprise agreement, which inherit its single-award, one-offer coding, the value share falls to 39 percent, and the second Trump administration share by award start falls from 60 to 9 percent. The three largest orders under the agreement are 73 percent of its obligations, and the five largest 82 percent.

## Limits

Obligations are not spending, and recent fiscal years are subject to reporting lag and revision. Fiscal years do not align with administrations. Competition coding comes from the latest transaction record and can differ from the original, and a sole-source coding for proprietary commercial software is not by itself evidence of dependency. The data do not show switching costs, data-rights or exit terms, interoperability, lifecycle cost, or the practical availability of alternatives, and they cannot separate lock-in from ordinary long-term demand. One order from a civilian agency appears under the agreement and should be checked against the Army's description of its use. The contract number was matched between a trade aggregator and the federal record, but the contract documents themselves were not read.

## What would test dependency

The contract's terms on data rights, exit, and interoperability, the sole-source justification, the pricing history of orders under the agreement, and the competition history of follow-on work.
