#   Copyright 2011 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# This has to be a separate type to enable collecting
Puppet::Type.newtype(:pgsql_database) do
  @doc = "Manage a database."
  ensurable
  newparam(:name) do
    desc "The name of the database."
  end
  newproperty(:owner) do
    desc "The owner of the database."

    defaultto "postgres"
  end
end
