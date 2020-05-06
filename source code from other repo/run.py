#!/usr/bin/python3.7

import argparse
import os

import ANF_transformer
from py_transform import transform_program
from tracing.runner import run_trace 

TRANSFORM_FILE = "transform.py"
TRANSFORM_FILE_FORMAT = "{}_transform.py"
TRACE_FILE_FORMAT = "{}.json"

def try_delete_file(file_path, verbose=False, force=True):
    if os.path.exists(file_path):
        if force:
            os.remove(file_path)
            if verbose:
                print("Deleted {}".format(file_path))
        else:
            raise Exception("{} already exists!".format(file_path))
 

def main():

    # Accepts one argument: the file containing the serverless function
    parser = argparse.ArgumentParser()
    parser.add_argument("serverless_function", 
            help="The path to the python file containing a serverless function")
    parser.add_argument("-v", "--verbose", action='store_true', 
            help="Print verbose output")
    parser.add_argument("-t", "--trace", action='store_true',
            help="Print verbose tracing output")
    parser.add_argument("-o", "--output_dir", help="A diretory to output " \
            "transformed python and the trace JSON file")
    parser.add_argument("-f", "--force", action='store_true',
            help="Delete output files if they already exist, including transform.py at current level")
    parser.add_argument("-a", "--arg", default=None, help="Argument for the serverless function")
    args = parser.parse_args()

    # Construct output paths
    transform_path = TRANSFORM_FILE_FORMAT.format(args.serverless_function.split('.py')[0])
    trace_path = TRACE_FILE_FORMAT.format(args.serverless_function.split('.py')[0])

    # Check if output files already exists, and if so, delete or raise exception
    try_delete_file(TRANSFORM_FILE, verbose=args.verbose, force=args.force)
    try_delete_file(transform_path, verbose=args.verbose, force=args.force)
    try_delete_file(trace_path, verbose=args.verbose, force=args.force)

    # Read in the file containing the serverless function
    with open(args.serverless_function, 'r') as f:
        function_code = f.read()
    if args.verbose:
        print("About to transform serverless function code. Original version:\n" \
                "========================================================\n"
                "{}\n"
                "========================================================\n".format(function_code))

    # transform the code
    transformed_code = transform_program(function_code)
    if args.verbose:
        print("Transformed code is:\n" \
                "========================================================\n"
                "{}\n"
                "========================================================\n".format(transformed_code))

    # write transform to the output directory
    if args.output_dir: 
        with open(transform_path, 'w') as f:
            f.write(transformed_code)
        print("Wrote transformed code to: {}".format(transform_path))


    # write transform to a local file
    with open(TRANSFORM_FILE, 'w') as f:
        f.write(transformed_code)
    print("Wrote transformed code to: {}".format(TRANSFORM_FILE))

    try:
        transform_module = __import__('transform')
        serverless_function = getattr(transform_module, 'serverless_function')
       
        if args.arg:
            ret_val, trace_json = run_trace(serverless_function, [int(args.arg)], verbose=args.trace)
        else:
            ret_val, trace_json = run_trace(serverless_function, verbose=args.trace)
        if args.trace:
            print("\n")

        if args.verbose:
            print("Traced code has return value {}, and trace is:\n" \
                "========================================================\n"
                "{}\n"
                "========================================================\n".format(ret_val, trace_json))

        # write trace to the output directory
        if args.output_dir: 
            with open(trace_path, 'w') as f:
                f.write(trace_json)
            print("Wrote trace to: {}".format(trace_path))

    finally:
        # Cleanup temporary file
        try_delete_file(TRANSFORM_FILE, verbose=args.verbose, force=True)


if __name__ == "__main__":
    main()
