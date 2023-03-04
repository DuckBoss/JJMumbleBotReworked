#!/usr/bin/env python3
from src.system_arguments import args_parser
from src.logging import init_logger


if __name__ == "__main__":
    sys_args = vars(args_parser.parse_args())
    init_logger(sys_args)
    from src.mumimo import MumimoService

    mumimo = MumimoService(sys_args)
