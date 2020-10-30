import argparse
import glob
import os
from lib.parser import get_file
from lib.generator import yara_image_rule_maker
from lib.render import yara_print_rule



class MFBot:
    """ Malicious File Bot Class """
    def __init__(self) -> None:
        args = MFBot.parse_args()
        self.yara_base_file = args.file
        self.image_name = None
        self.idat = args.idat
        self.jpgsos = args.jpgsos
        self.dir = args.dir
        self.dirhash = []
        self.name = args.name
        project_info_data = """
-- Halogen ------------------------------------
Authors: Wyatt Roersma, Kyle Eaton, Devin Smith
-----------------------------------------------
        """

    @staticmethod
    def parse_args()-> iter:
        """ Parse any options passed to the the script """
        parser_args = argparse.ArgumentParser(description="Halogen:  Automatically create yara \
            rules based on images embedded in office documents.")
        parser_args.add_argument("-f", "--file", help="File to parse")
        parser_args.add_argument("-d", "--directory", dest="dir", help="directory to scan \
            for image files.")
        parser_args.add_argument("-n", "--rule-name", dest="name", help="specify a custom \
            name for the rule file")
        parser_args.add_argument("--png-idat", dest="idat", help="For PNG matches, instead \
            of starting with the PNG file header, start with the IDAT chunk.", action='store_true')
        parser_args.add_argument("--jpg-sos", dest="jpgsos", help="For JPG matches, skip \
            over the header and look for the Start of Scan marker, \
            and begin the match there.", action='store_true')
        args = parser_args.parse_args()
        if (args.file is None) and (args.dir is None):
            parser_args.print_help()
            exit(1)
        return args

    def run(self):
        """mfbot.run() is the core function to call that will return all information
        generated by mfbot.
        returns: rule_dict - dictionary of rules. """
        self.get_file = get_file(self)
        rule_dict = yara_image_rule_maker(self)
        if rule_dict is not None:
            return rule_dict

    def print_yara_rule(self, rule_list):
        """ prints the yara rule by reading in a list of dicts, and iterating over that.
        parameter: rule_list - list of rules to print. """
        yara_print_rule(self, rule_list)

    def dir_run(self):
        """ runs through the process with a directory instead of a single file.
        returns: combo list. """
        filelist = glob.glob(self.dir + "/*")
        combo = []
        for f in filelist:
            if os.path.isfile(f):
                self.image_name = None
                self.yara_base_file = f
                self.get_file = get_file(self)
                self.dirhash.append(self.get_file[0])
                rule_dict = yara_image_rule_maker(self)
                if rule_dict is not None:
                    for i in rule_dict:
                        if i not in combo:
                            combo.append(i)
            else:
                pass
        return combo
