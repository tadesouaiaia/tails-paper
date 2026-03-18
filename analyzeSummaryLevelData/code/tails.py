#!/usr/bin/env python3
import argparse, sys, os, re, shlex

def qc_run(args, command_line):   
    from src.tail_qc.qcRun import qcRun
    out_dir = os.path.dirname(args.out) 
    if out_dir: os.makedirs(out_dir, exist_ok=True) 
    qcRun(args, command_line).go() 

def fig_gen(args, command_line):  
    from src.tail_fig.figGen import figGen
    out_dir = os.path.dirname(args.out) 
    if out_dir: os.makedirs(out_dir, exist_ok=True) 
    figGen(args, command_line).go() 


def build_parser():
    parser = argparse.ArgumentParser(prog="tails")
    sub = parser.add_subparsers(dest="cmd")

    # ----- qc -----
    qc = sub.add_parser("qc", help="QC workflows")
    qc_sub = qc.add_subparsers(dest="qc_cmd")

    qc_common = argparse.ArgumentParser(add_help=False)
    qc_common.add_argument("--in", dest="infile", required=True, type=argparse.FileType("r"))
    qc_common.add_argument("--out", required=True, type=str)
    qc_common.add_argument("--silent",action="store_true",help="Suppress non-essential output")
    qc_common.add_argument("--verbose",action="store_true",help="Enable verbose output")
    qc_common.add_argument("--showVariables",action="store_true",help="Show Variable Information") 

    p = qc_sub.add_parser("load", parents=[qc_common], help="Load QC files and initialize QC outputs")
    p.add_argument("--qcFiles", required=True, nargs="+", type=argparse.FileType("r"))
    p.add_argument("--allowMissing",action="store_true",help="Suppress non-essential output")
    p.set_defaults(func=qc_run)

    p = qc_sub.add_parser("filter", parents=[qc_common],help="Filter traits")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--applyFilters',type=str) 
    group.add_argument('--useStandardFilters',action='store_true') 



    p.add_argument('--configFile',type=argparse.FileType('r')) 
    p.add_argument('--dupeFile',type=argparse.FileType('r')) 
    p.add_argument('--dupeCutoff', type=float,default=0.99,metavar='',help="Duplication Cutoff (0.99 Default)")
    p.add_argument('--dupeTieBreak',type=str,default='N') 
    p.set_defaults(func=qc_run)

    
    p = qc_sub.add_parser("run", parents=[qc_common],help="Load QC and files and run filters")
    
    p.add_argument("--qcFiles", required=True, nargs="+", type=argparse.FileType("r"))
    p.add_argument("--allowMissing",action="store_true",help="Suppress non-essential output")
    
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--applyFilters',type=str) 
    group.add_argument('--useStandardFilters',action='store_true') 
    
    p.add_argument('--configFile',type=argparse.FileType('r')) 
    p.add_argument('--dupeFile',type=argparse.FileType('r')) 
    p.add_argument('--dupeCutoff', type=float,default=0.99,metavar='',help="Output Prefix")
    p.add_argument('--dupeTieBreak',type=str,default='N') 
    p.set_defaults(func=qc_run)

    




    # ----- figs (stage-1: just for help/menu) -----
    gen = sub.add_parser("gen",  help="Figure/table generation")
    # We do NOT add required --vals/--pts here, because we want `tails figs`
    # to show a menu instead of erroring.
    return parser, qc, gen


def figs_menu(figs_parser):
    # A "fake" menu that looks like subparser help
    figs_parser.print_usage()
    print("\npositional arguments:")
    print("  {all,all-plots,all-tables,plotN,tableN} ...")
    print("    all         Generate all figures, extended data, csv tables")
    print("    figs        Generate all main figs (1-5)")
    print("    figN        Generate main figures N, (e.g., fig1, fig2)")
    print("    csv         Generate csv tables only ")
    print("\nrequired arguments (for commands other than help/menu):")
    print("  --in   INPUT              Qced Trait File (output from QC)")
    print("  --vals VALS [VALS ...]    One or more .vals files")
    print("  --pts  PTS  [PTS  ...]    One or more .pts files")
    print("\noptions:")
    print("  -h, --help  show this help message and exit")


def parse_figs_args(argv):
    # Full figs parser (stage-2): requires vals/pts and accepts `what`
    p = argparse.ArgumentParser(prog="tails figs")
    p.add_argument("which", type=str, help="all|all-plots|all-tables|plotN|tableN")
    p.add_argument("--in", dest='infile',required=True, type=argparse.FileType("r"))
    p.add_argument("--vals", required=True, nargs="+", type=argparse.FileType("r"))
    p.add_argument("--pts",  required=True, nargs="+", type=argparse.FileType("r"))
    p.add_argument("--silent",action="store_true",help="Suppress non-essential output")
    p.add_argument("--simPath", type=str, help="simulation results") 
    p.add_argument("--dpi", type=int, default=500, help="Figure DPI") 
    p.add_argument("--indexTraits", type=int, nargs=4, help="Four Index Traits", default=[30810, 30070, 30020, 20015]) 
    p.add_argument("--out", type=str, default='', help="Output Path/Prefix") 
    return p.parse_args(argv)


def validate_figs_what(which: str) -> bool:
    wx = which.upper() 
    if wx in {"ALL",'MAIN','MAINS','MAIN-FIGS','MAIN-FIGURES','FIGS','EXCEL','CSV','CSVS','XTD','XTDS','EXT','EXTS','EXTENDED-DATA'}: return True
    elif wx in {"SLIM","SIM","SIMS"}: return True
    for x in ['FIG','SUP','TAB','MAIN','EXT','XTD']: 
        if wx[0:len(x)] == x: return True 
    sys.stderr.flush()
    sys.stdout.write('Invalid Figure: Try: ./tails gen all or tails gen main2\n') 
    return False


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    
    command_line = " ".join(shlex.quote(x) for x in sys.argv)
    parser, qc_parser, figs_parser = build_parser()

    # First pass: only parse top-level command (and qc subcommands normally)
    args, rest = parser.parse_known_args(argv)
    if args.cmd is None:
        parser.print_help()
        return 0
    

    if args.cmd == "qc":
        # Let normal argparse handle qc fully (and show qc help if missing subcmd)
        args = parser.parse_args(argv)
        if args.qc_cmd is None:
            qc_parser.print_help()
            return 0
        args.func(args, command_line)
        return 0

    if args.cmd == "gen":
        # If user typed just `tails figs` or `tails figs help`, show menu.
        if len(rest) == 0 or (len(rest) == 1 and rest[0] in {"help", "-h", "--help"}):
            figs_menu(figs_parser)
            return 0
        # Otherwise parse figs properly (requires vals/pts)
        figs_args = parse_figs_args(rest)
        if os.path.isdir(figs_args.out) and not figs_args.out.endswith(os.sep):  figs_args.out += os.sep  
        if not validate_figs_what(figs_args.which):
            figs_menu(figs_parser)
            return 2
        fig_gen(figs_args, command_line)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
