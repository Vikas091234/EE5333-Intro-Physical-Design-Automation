# EE5333 – Introduction to Physical Design Automation
## Detailed Routing Project – Results and Observations

## 1. Experimental Evaluation

The final implementation was evaluated on seven supplied benchmark designs: `add5`, `c17`, `c432`, `c499`, `c6288`, `c7552`, and `spm`. For each benchmark, the detailed router was executed using the corresponding DEF, LEF, and GUIDE files. The generated DEF was then checked using `checker.py`.

## 2. Results

| Benchmark | Guide Nets | Routed Nets | Open Nets | Routing Time (s) | Spacing Violations |
|---|---:|---:|---:|---:|---:|
| add5 | 61 | 60 | 0 | 0.29 | 52 |
| c17 | 23 | 22 | 0 | 0.22 | 20 |
| c432 | 198 | 197 | 0 | 0.63 | 291 |
| c499 | 363 | 362 | 0 | 1.48 | 564 |
| c6288 | 1526 | 1525 | 0 | 4.08 | 3236 |
| c7552 | 1592 | 1591 | 0 | 11.77 | 3991 |
| spm | 308 | 307 | 0 | 1.09 | 873 |

The router reports one fewer routed net than the total number of nets listed in the GUIDE files for every benchmark. The checker reports **zero open nets for every benchmark**, so all nets considered routable by the implementation were successfully connected.

## 3. Connectivity Observations

The most significant result is that every benchmark achieved **Open nets = 0**. This indicates that the implementation successfully established connectivity for all routed nets across the complete benchmark set, including the larger designs `c6288` and `c7552`.

## 4. Runtime Observations

Routing time increases as benchmark size and routing complexity increase. The smallest measured time was 0.22 s for `c17`, while `c7552`, with 1591 routed nets, required 11.77 s.

The measured routing times were:

- `add5`: 0.29 s
- `c17`: 0.22 s
- `c432`: 0.63 s
- `c499`: 1.48 s
- `c6288`: 4.08 s
- `c7552`: 11.77 s
- `spm`: 1.09 s

The implementation therefore completes the supplied benchmark suite within practical execution times.

## 5. Spacing Violation Observations

Although connectivity was achieved for all benchmarks, the checker reported spacing violations for every benchmark.

The reported counts were:

- `c17`: 20
- `add5`: 52
- `c432`: 291
- `c499`: 564
- `spm`: 873
- `c6288`: 3236
- `c7552`: 3991

The checker output contains both **net-to-net** and **net-to-obstruction** spacing violations. Therefore, the implementation should **not** be described as completely DRC-clean. Its strongest demonstrated property is successful connectivity, while geometric spacing compliance remains an area for improvement.

The number of reported violations increases substantially for the larger benchmarks. This indicates that congestion and geometric interactions become more difficult as the number of routed nets increases.

## 6. Interpretation

The results demonstrate a clear trade-off in the current routing strategy. The router successfully prioritizes connectivity: all seven benchmarks finish with zero open nets. However, as routing complexity increases, more spacing conflicts are reported by the checker.

This suggests that the current heuristics are effective at finding routes that establish connectivity, but route selection and spacing enforcement require further refinement to consistently avoid all geometric conflicts.

The results also show that the number of spacing violations does not simply depend on runtime; it is strongly affected by the geometry and congestion of each individual design. For example, `spm` has 307 routed nets and 873 reported violations, whereas `c499` has 362 routed nets and 564 violations.

## 7. Limitations

The experimental results establish successful connectivity, but they do not establish complete DRC correctness.

The current implementation has the following limitations:

- Spacing violations remain in all evaluated benchmarks.
- Larger designs generally produce substantially more spacing conflicts.
- Both net-to-net and net-to-obstruction violations are present.
- Further improvement is required in spacing enforcement and congestion-aware route selection.

## 8. Conclusion

The final implementation successfully routes all seven evaluated benchmark designs with **zero open nets**. Routing time ranges from **0.22 s to 11.77 s** across the benchmark suite.

The main remaining limitation is spacing-rule compliance. The checker reports between **20 and 3991 spacing violations**, depending on the benchmark, with the largest designs generally exhibiting substantially more conflicts.

Overall, the implementation demonstrates effective connectivity routing and practical runtime on the supplied benchmarks. The experimental results clearly identify spacing enforcement and congestion handling as the primary areas for future improvement.
