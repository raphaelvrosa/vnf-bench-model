Description of VNF-BD example messages in Gym

                                                Deploy VNF-BD Scenario
                        +-------+                 +------------------+
                        |       |                 |                  |
                        +       v                 +                  v
Layout+----->  Build VNF-BD   (check VNF-BD instances)          Orchestrator
                                ^          +     ^                  +  +
                                |          |     +------------------+  |
                                |          |     Built VNF-BD Scenario |
                                |          |                           |
                                |          |                           |
                                |          |         Hello             |
                                |          |  +------------------>     v
                                |          v  +                   (Manager)<------+
                                |     Greetings<---------------+                  |
                                |          +         Info           ^ +           v
                                |          v                        | |  (Agents / Monitors)
                                |      Tasks+-------------------+---+ |
                                |          +         Task             |
                                |          v                          |
                                +-----+Status(VNF-BD)<+---------------+
                                Instances +               Report
                                            |Finished
                                            v
VNF-BR  <----------+Build VNF-BR<------+Build VNF-PP