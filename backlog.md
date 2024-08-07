# Filter playground backlog

* Add ripple/passband input fields
* Fix bode plot margins
* Clarify cascading/summing for the output
* Move input parameters as third tab with Bode/PZ
    * Merge DualGraphWidget into InputFilterWidget
* Move cascade output as first tab of input filters
    * Rename InputWidget as CascadeWidget
    * Add first tab with OutputBodeGraphWidget
* Duplicate this new input section
    * Make InputWidget laid out as VBox and include 2 CascadeWidget
* Make output the sum to these two cascades