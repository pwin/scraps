import argparse
import sys
import glob
import re 
import pathlib

def visualise_tarql(path_in, path_out):
    tarqlFileContent = open(path_in, "rb").read()
    tarqlFileContentText = tarqlFileContent.decode("utf-8")
    output_file = open(path_out, "w")

    prefixesPattern = r".*prefix.*"
    allPrefixes = re.findall(prefixesPattern, tarqlFileContentText, re.IGNORECASE)

    allPrefixes1 = [f"@{x}.".replace("\r"," ") for x in allPrefixes]

    for x in allPrefixes1:
        print(x, file=output_file)
    print("@base <http://tarqlviz.org/> .", file=output_file)
    print("@prefix : <#> .", file=output_file)
    corePattern = re.compile(r'CONSTRUCT[\n\W]+\{([\n\W\w]+)\}[\n\W\w]+WHERE[\n\W]+\{?', re.MULTILINE|re.IGNORECASE)
    matches = [m.groups() for m in corePattern.finditer(tarqlFileContentText)]
    #print(matches)
    #for x in matches:
    #    print(x)
    for x in matches:
        print(x[0].replace("?",":"), file=output_file)


def main(arguments):
    parser = argparse.ArgumentParser(
        prog='Visualise TARQL Pre-processor',
        description='Converts the TARQL Pattern "construct" statements to Turtle.',
        epilog='version 0.1')
    parser.add_argument('tarql_file')  # positional argument
    parser.add_argument('-o', '--output',
                        default=None)  # output folder
    args = parser.parse_args()
    print(args.tarql_file)
    if args.output:
        visualise_tarql(args.tarql_file, args.output)
    else:
        visualise_tarql(args.tarql_file, args.tarql_file + ".ttl")

def run_tool():
    main(sys.argv[1:] if len(sys.argv) > 1 else ['-h'])


if __name__ == "__main__":
    run_tool()
