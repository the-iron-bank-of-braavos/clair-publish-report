import json
from junit_xml import TestSuite, TestCase
import os
import argparse
import logging

logger = logging.getLogger('clair_scanner_converter')
logger.setLevel(logging.WARN)
console_logger = logging.StreamHandler()
console_logger.setLevel(logging.WARN)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_logger.setFormatter(formatter)
logger.addHandler(console_logger)

def parse_args():
    parser = argparse.ArgumentParser(description="Process Json File")
    parser.add_argument("clairfile", type=str, default=None, help="Location of clair scanner ouptut file to convert to cucumber.json")
    parser.add_argument("--output", type=str, default=None, help="name of output file to store in new format. Defaults to clair inputfile")
    args = parser.parse_args()
    if not args.output:
        logger.warning("No output file specified, replacing input file.")
        args.output = args.clairfile
    return args

def main():
    cwd = os.getcwd()
    args = parse_args()
    try:
        if os.path.exists(args.clairfile):
            with open(args.clairfile) as clairfile:
                clair_parsed_file = json.load(clairfile)
    except:
        logger.exception("Failed to parse clair / clair_error file.  Exiting.")

    current_suite = current_suite = TestSuite(name="Scanner Results")
    test_suites = []
    test_suites.append(current_suite)
    for idVulnerability in clair_parsed_file["vulnerabilities"]:
            name=clair_parsed_file['vulnerabilities'][idVulnerability]["name"]
            description=clair_parsed_file['vulnerabilities'][idVulnerability]["description"]
            new_step = TestCase(
                name=clair_parsed_file['vulnerabilities'][idVulnerability]["id"],
                classname=clair_parsed_file['vulnerabilities'][idVulnerability]["name"],
                status="unapproved",
                url=clair_parsed_file['vulnerabilities'][idVulnerability]["links"])

            new_step.add_failure_info(message=f"{name}.{description}")
            current_suite.test_cases.append(new_step)
        # try to write new file
    try:
        with open(args.output, 'w') as outfile:
            outfile.write(TestSuite.to_xml_string(test_suites))
    except Exception as ex:
        logger.exception("Filed saving file: " + ex)


if __name__ == "__main__":
    main()
#    for idVulnerability  in clair_parsed_file['vulnerabilities']:
#         record = clair_parsed_file['vulnerabilities'][idVulnerability]['name']
#         logger.warning(record)

