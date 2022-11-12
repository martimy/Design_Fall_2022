"""
Copyright 2022 Maen Artimy

"""

import os
import pyparsing as pp
import pandas as pd


# This code verifies if a Cisco device configuration includes SNMP configuration
# similar to the following:
#
# snmp-server community public RO
# snmp-server community private RW
# snmp-server location my_location
# snmp-server contact admin@domain


SNMP_END_MARKER = pp.LineEnd().suppress()
REMAINDER = pp.SkipTo(pp.LineEnd())

NUM = 5
PATH = 'lab/configs'
READ_COL = 'Read'
ref_string = set(["dcread"])

class SNMPValues():
    """
    Collects SNMP values from configuration
    """

    def __init__(self, cfg_list):
        self.cfg_list = cfg_list
        self.results = []

    def __snmp_parser(self, text):
        """
        Parse SNMP configuration.
        """

        SNMP_START_MARKER = pp.LineStart() + pp.Keyword("snmp-server").suppress()
        SNMP_COMMUNITY = pp.Keyword("community").suppress()
        SNMP_LOCATION = pp.Keyword("location").suppress()
        SNMP_CONTACT = pp.Keyword("contact").suppress()
        SNMP_STRING = pp.Word(pp.alphanums, asKeyword=True)

        snmp_ro = SNMP_START_MARKER + SNMP_COMMUNITY + \
            SNMP_STRING("Read") + pp.Keyword("RO").suppress()
        snmp_rw = SNMP_START_MARKER + SNMP_COMMUNITY + \
            SNMP_STRING("Write") + pp.Keyword("RW").suppress()
        snmp_location = SNMP_START_MARKER + \
            SNMP_LOCATION + REMAINDER("Location")
        snmp_contact = SNMP_START_MARKER + SNMP_CONTACT + REMAINDER("Contact")

        policy_def = snmp_ro ^ snmp_rw ^ snmp_location ^ snmp_contact
        return policy_def.searchString(text)

    def __parse(self, device, cfg_lines):
        """
        Parse configuration lines and return dict

        """

        # parse text and return a list of dict
        snmp_lines = self.__snmp_parser(cfg_lines)
        snmp_list = [p.asDict() for p in snmp_lines if p]

        # merge all dictionaries but there may be
        # multiple read and readwrite communities
        merged = {'Node': device, 'Read': [],
                  'Write': [], 'Location': '', 'Contact': ''}
        for lines in snmp_list:
            for key, value in lines.items():
                if key in ['Read', 'Write']:
                    merged[key].append(value)
                else:
                    merged[key] = value
        return merged

    def answer(self):
        """
        returns a list if parsed values

        """

        for filename in self.cfg_list:
            with open(filename, 'r') as fgfile:
                cfg = fgfile.read()
                device = os.path.basename(filename)
                self.results.append(self.__parse(device, cfg))
        return self

    def frame(self):
        """
        Format as pandas frame
        """

        return pd.DataFrame(self.results)


def test_snmp_properties(cfg_files):
    """
    Testing correct snmp configuration

    Test fails if snmp configuration is missing or incomplete
    """

    # Ask SNMP questions
    snmp_parameters = SNMPValues(cfg_files).answer().frame()
    
    # check if all nodes are present
    assert len(snmp_parameters.index) == NUM, f"Expecting {NUM} lines, \
           found {len(snmp_parameters.index)}:\n{snmp_parameters}"

    # Find nodes that have no SNMP servers configured
    snmp_violators = snmp_parameters[snmp_parameters[READ_COL].apply(
        lambda x: len(x) == 0)]
    assert snmp_violators.empty, f"Missing SNMP configuration:\
        \n{snmp_violators}"

    # Find nodes with misconfigured read community string
    community_violators = snmp_parameters[snmp_parameters[READ_COL].apply(
        lambda x: len(ref_string.intersection(set(x))) == 0)]
    assert community_violators.empty, f"Missing or incorrect community string:\
        \n{community_violators}"


if __name__ == "__main__":

    # Get all files in the given path
    files_list = [os.path.join(PATH, path) for path in os.listdir(
        PATH) if os.path.isfile(os.path.join(PATH, path))]

    assert files_list, "No configuration files"

    test_snmp_properties(files_list)
    print("All checks passed!")