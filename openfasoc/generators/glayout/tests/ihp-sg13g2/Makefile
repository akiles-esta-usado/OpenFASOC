PDK=ihp-sg13g2

KLAYOUT_EXE		= $(shell command -v klayout)
KLAYOUT_ARGS	= -c klayoutrc -t -e
KLAYOUT			= $(KLAYOUT_EXE) $(KLAYOUT_ARGS)
KLAYOUT_CLI     = $(KLAYOUT) -b -zz

XSCHEM_EXE		= $(shell command -v xschem)
XSCHEM_ARGS     = --rcfile $(PDK_ROOT)/$(PDK)/libs.tech/xschem/xschemrc
XSCHEM          = $(XSCHEM_EXE) $(XSCHEM_ARGS)

TOP_GDS         ?= $(realpath $(TOP)/$(TOP).gds)
TOP_SCH         ?= $(realpath $(TOP)/$(TOP).sch)
TOP_SPICE       ?= $(realpath $(TOP)/$(TOP).spice)


klayout:
	$(KLAYOUT) $(TOP_GDS)


klayout-script:
	$(KLAYOUT_CLI) -r $(TOP)


xschem:
	$(XSCHEM) $(TOP_SCH)


# --help -h                 Displays this help message.
# --layout=<layout_path>    Specifies the file path of the input GDS file.
# --netlist=<netlist_path>  Specifies the file path of the input netlist file.
# --run_dir=<run_dir_path>  Run directory to save all the generated results [default: pwd]
# --topcell=<topcell_name>  Specifies the name of the top cell to be used.
# --run_mode=<run_mode>     Selects the allowed KLayout mode. (flat, deep). [default: flat]
# --no_net_names            Omits net names in the extracted netlist.
# --spice_comments          Includes netlist comments in the extracted netlist.
# --net_only                Generates netlist objects only in the extracted netlist.
# --no_simplify             Disables simplification for both layout and schematic netlists.
# --no_series_res           Prevents simplification of series resistors for both layout and schematic.
# --no_parallel_res         Prevents simplification of parallel resistors for both layout and schematic.
# --combine_devices         Enables device combination for both layout and schematic netlists.
# --top_lvl_pins            Creates pins for top-level circuits in both layout and schematic netlists.
# --purge                   Removes unused nets from both layout and schematic netlists.
# --purge_nets              Purges floating nets from both layout and schematic netlists.
# --verbose                 Enables detailed rule execution logs for debugging purposes.

klayout-lvs:
	python $(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech/lvs/run_lvs.py \
		--layout=$(TOP_GDS) \
		--netlist=$(TOP_SPICE) \
		--topcell=$(TOP) \
		--run_mode=deep \
		--run_dir=./tmp/ \
		--verbose


# in_gds                 path to the GDS layout to check (required in batch mode)
# cell                   name of the cell to check
# log_file               path to the log file [default: no log file]
# report_file            path to the report database [default: sg13g2_maximal.lyrdb in the script directory]
# offGrid                
# density                
# filler                 
# noRecommendedRules     
# sanityRules            
# checkDensityRules      

klayout-drc:
	$(KLAYOUT_CLI) -r $(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech/drc/sg13g2_maximal.lydrc \
		-rd in_gds=$(TOP_GDS) \
		-rd cell=$(TOP) \
		-rd log_file=./tmp/$(TOP)_drc.log \
		-rd report_file=./tmp/$(TOP).lyrdb \
		-rd offGrid=true \
		-rd density=false \
		-rd filler=true \
		-rd noRecommendedRules=true \
		-rd sanityRules=true \
		-rd checkDensityRules=true
	
	$(KLAYOUT) $(TOP)/$(TOP).gds -m ./tmp/$(TOP).lyrdb



klayout-drc-full:
	$(KLAYOUT_CLI) -r $(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech/drc/sg13g2_maximal.lydrc \
		-rd in_gds=$(TOP_GDS) \
		-rd cell=$(TOP) \
		-rd log_file=./tmp/$(TOP)_drc.log \
		-rd report_file=./tmp/$(TOP).lyrdb \
		-rd offGrid=false \
		-rd density=false \
		-rd filler=true \
		-rd noRecommendedRules=true \
		-rd sanityRules=true \
		-rd checkDensityRules=true
	
	$(KLAYOUT) $(TOP)/$(TOP).gds -m ./tmp/$(TOP).lyrdb


klayout-drc-cli:
	$(KLAYOUT_CLI) -r $(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech/drc/sg13g2_maximal.lydrc \
		-rd in_gds=$(TOP_GDS) \
		-rd cell=$(TOP) \
		-rd log_file=./tmp/$(TOP)_drc.log \
		-rd report_file=./tmp/$(TOP).lyrdb \
		-rd offGrid=true \
		-rd density=false \
		-rd filler=true \
		-rd noRecommendedRules=true \
		-rd sanityRules=true \
		-rd checkDensityRules=true


glayout:
	python $(TOP).py && make TOP=$(TOP) klayout-drc




glayout-test:
	python test_via.py >/dev/null 2>/dev/null
	make TOP=test_via klayout-drc-cli | grep -v 'Number of DRC errors: 0'

	python test_via_stack.py >/dev/null 2>/dev/null
	make TOP=test_via_stack klayout-drc-cli | grep -v 'Number of DRC errors: 0'

	python test_via_array.py >/dev/null 2>/dev/null
	make TOP=test_via_array klayout-drc-cli | grep -v 'Number of DRC errors: 0'

	python test_tapring.py >/dev/null 2>/dev/null
	make TOP=test_tapring klayout-drc-cli | grep -v 'Number of DRC errors: 0'

	python test_nmos.py >/dev/null 2>/dev/null
	make TOP=test_nmos klayout-drc-cli | grep -v 'Number of DRC errors: 0'

	python test_pmos.py >/dev/null 2>/dev/null
	make TOP=test_pmos klayout-drc-cli | grep -v 'Number of DRC errors: 0'