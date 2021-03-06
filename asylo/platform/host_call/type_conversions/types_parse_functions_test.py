#
# Copyright 2019 Asylo authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Tests for types_parse_functions."""

from unittest import main
from unittest import TestCase

from asylo.platform.host_call.type_conversions.types_parse_functions import define_enum
from asylo.platform.host_call.type_conversions.types_parse_functions import get_enums
from asylo.platform.host_call.type_conversions.types_parse_functions import get_includes_as_include_macros
from asylo.platform.host_call.type_conversions.types_parse_functions import get_includes_in_define_macro
from asylo.platform.host_call.type_conversions.types_parse_functions import get_prefix
from asylo.platform.host_call.type_conversions.types_parse_functions import include
from asylo.platform.host_call.type_conversions.types_parse_functions import set_prefix


class TypesParseFunctionsTest(TestCase):
  """Tests for types functions."""

  def test_get_enums_with_only_default_vals(self):
    define_enum('TestEnum', ['a', 'b'])
    self.assertEqual(
        get_enums(),
        '#define ENUMS_INIT \\\n{"TestEnum", {0, 0, false, {{a, "a"}, {b, "b"}}}}'
    )

  def test_get_enums_with_all_vals(self):
    define_enum('TestEnum', ['a'], 1, 2, True)
    self.assertEqual(
        get_enums(),
        '#define ENUMS_INIT \\\n{"TestEnum", {1, 2, true, {{a, "a"}}}}')

  def test_prefix(self):
    prefix_string = 'test_prefix'
    set_prefix(prefix_string)
    self.assertEqual(get_prefix(),
                     'const char prefix[] = "{}";\n'.format(prefix_string))

  def test_include_exceptions(self):
    with self.assertRaises(ValueError):
      include('<my_header_file>')
    with self.assertRaises(ValueError):
      include('"my_header_file"')
    with self.assertRaises(ValueError):
      include('#include "myheaderfile.h"')

  def test_get_includes(self):
    include('iostream')
    include('stdio')
    self.assertEqual(get_includes_as_include_macros(),
                     '#include <iostream>\n#include <stdio>\n')
    self.assertEqual(get_includes_in_define_macro(),
                     '#define INCLUDES "iostream", \\\n"stdio"')


if __name__ == '__main__':
  main()
