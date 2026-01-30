# vunit-json-for-vhdl

A VUnit package providing JSON parsing and querying capabilities for VHDL.

## Overview

vunit-json-for-vhdl is based on the [JSON-for-VHDL](https://github.com/Paebbels/JSON-for-VHDL) project which provides the core VHDL functionality to operate on JSON data structures. In addition, vunit-json-for-vhdl provides integration support for exchanging JSON data between the VUnit Python run script and the simulator, using string generics as the transport mechanism. This makes it straightforward to pass structured configuration data from Python into VHDL testbenches.

## Installation

```bash
pip install vunit-json-for-vhdl
```

## Basic Example

For more in-depth examples of the VHDL part, see the [JSON-for-VHDL](https://github.com/Paebbels/JSON-for-VHDL) project.

Below is an example of how the VUnit run script can pass JSON data structures to the testbench.

```python
from vunit import VUnit

# By importing vunit_json_for_vhdl, we get access to the Python helper
# functions of the project. This is not necessary if all you need
# are the VHDL parts.
import vunit_json_for_vhdl

vu = VUnit.from_argv()
vu.add_vhdl_builtins()

# Add the VHDL parts
vu.add_component("vunit-json-for-vhdl")

# By grouping all testbench configurations in a dictionary, we keep the
# testbench generic declaration short and there is no need to update it
# when adding new configurations.
tb_cfg = dict(image_size=(384, 216), enable_compression=True)

# Converting the testbench configuration dictionary into JSON would
# result in the following string:
#
# '{"image_size": [384, 216], "enable_compression": true}'
#
# All the special characters become a problem when passing the string
# as a generic to the simulator. Different simulators have different
# limitations on the allowed characters in generics and how they are
# escaped. To avoid these issues, we need a simpler hexadecimal string
# representation of the JSON string.
tb_cfg_str = vunit_json_for_vhdl.to_str(tb_cfg)

# The configuration generic is passed to the testbench in the normal way,
# for example:
my_lib = vu.add_library("my_lib")
my_lib.add_source_files(path / to / my / source / files / "*.vhd")
my_tb = my_lib.entity("my_tb")
my_tb.set_generic("tb_cfg", tb_cfg_str)

vu.main()
```

Below is an example of how the VHDL testbench can extract the individual fields of the JSON data structure.

```vhdl
library vunit_lib;
context vunit_lib.vunit_context;

library json;
context json.json_ctx;

entity my_tb is
  generic (
    runner_cfg : string;
    tb_cfg   : string
  );
end entity;

architecture tb of my_tb is
begin
  test_runner: process is
    constant tb_cfg_json : T_JSON := jsonLoad(tb_cfg);
    constant image_size : integer_vector :=
      jsonGetIntegerArray(tb_cfg_json, "image_size");
    constant enable_compression : boolean :=
      jsonGetBoolean(tb_cfg_json, "enable_compression");
  begin
    test_runner_setup(runner, runner_cfg);

    for i in 0 to image_size'length-1 loop
      info(
        "Image size [" & to_string(i) & "]: " &
        to_string(image_size(i))
      );
    end loop;
    info("Enable compression: " & to_string(enable_compression));

    test_runner_cleanup(runner);
  end process;
end architecture;
```


