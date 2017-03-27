#!/usr/bin/env python

###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = "Pierre Chaumeil"
__copyright__ = "Copyright 2017"  
__credits__ = ["Pierre Chaumeil"]
__license__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "Pierre Chaumeil"
__email__ = "uqpchaum@uq.edu.au"
__status__ = "Development"


import argparse
import sys
from gtdbtk import gtdbtk

from biolib.logger import logger_setup
from biolib.misc.custom_help_formatter import CustomHelpFormatter


def printHelp():
    print '''\
    
              ...::: GTDB-Tk v%s :::...

  Workflows:
    de_novo_wf  -> Infer a de novo tree, root, and decorate with taxonomy
                   (indentify -> align -> infer -> root -> decorate)
    classify_wf -> Classify genomes by placement in GTDB reference genome tree
                   (identify -> align -> classify)
    
  Methods:
    identify -> Identify marker genes in genome
    align    -> Create multiple sequence alignment
    infer    -> Infer tree from multiple sequence alignment
    classify -> Determine taxonomic classification of genomes
    root     -> Root tree using an outgroup
    decorate -> Decorate tree with GTDB taxonomy
      
  Use: gtdbtk <command> -h for command specific help
    ''' % __version__


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='gtdb', add_help=False, conflict_handler='resolve')
    parser.add_argument('-t', '--threads', type=int, default=1, help="number of threads/cpus to use.")
    parser.add_argument('-f', '--force', action="store_true", default=False, help="overwrite existing files without prompting.")

    subparsers = parser.add_subparsers(help="--", dest='subparser_name')

    # identify marker genes in genomes
    identify_parser = subparsers.add_parser('identify', conflict_handler='resolve',
                                            formatter_class=CustomHelpFormatter,
                                            help='Identify marker genes in genome.')
                          
    mutex_identify = identify_parser.add_argument_group('mutually exclusive required arguments')
    mutex_group = mutex_identify.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument('--genome_dir',
                                help="directory exclusively containing genome files in FASTA format") 
    mutex_group.add_argument('--batchfile',
                                help="file describing genomes - tab separated in 2 columns (FASTA file, genome ID)")
    
    required_identify = identify_parser.add_argument_group('required named arguments')
    required_identify.add_argument('--out_dir', required=True,
                                    help="directory to output files")

    optional_identify = identify_parser.add_argument_group('optional arguments')
    optional_identify.add_argument('--proteins', action="store_true",
                                    help='genome files contains proteins')
    optional_identify.add_argument('--prefix', default='gtdbtk',
                                    help='desired prefix for output files')
    optional_identify.add_argument('--cpus', default=1, type=int,
                                    help='number of CPUs to use')
    optional_identify.add_argument('-h', '--help', action="help",
                                    help="show help message")
    
    # create multiple sequence alignment
    align_parser = subparsers.add_parser('align', conflict_handler='resolve',
                                         formatter_class=CustomHelpFormatter,
                                         help='Create multiple sequence alignment.',)
                                         
    mutex_align = align_parser.add_argument_group('mutually exclusive required arguments')
    mutex_group = mutex_align.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument('--genome_dir',
                                help="directory exclusively containing genome files in FASTA format") 
    mutex_group.add_argument('--batchfile',
                                help="file describing genomes - tab separated in 2 columns (FASTA file, genome ID)")
    

    required_align = align_parser.add_argument_group('required named arguments')
    required_align.add_argument('--identify_dir', required=True,
                                       help="output directory of 'identify' command")
    required_align.add_argument('--out_dir', required=True,
                                       help='directory to output files')

    mutual_align = align_parser.add_argument_group('mutually exclusive required arguments')
    mutex_group = mutual_align.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument('--bac_ms', action='store_true', help='align bacterial marker genes')
    mutex_group.add_argument('--ar_ms', action='store_true', help='align archaeal marker genes')

    optional_align = align_parser.add_argument_group('optional arguments')
    optional_align.add_argument('--taxa_filter',
                                       help=('Filter genomes to taxa (comma separated) within '
                                            + 'specific taxonomic groups (e.g., d__Bacteria '
                                            + 'or p__Proteobacteria, p__Actinobacteria).'))
    optional_align.add_argument('--min_perc_aa', type=float, default=50,
                                       help='filter genomes with an insufficient percentage of AA in the MSA')
    optional_align.add_argument('--consensus', type=float, default=25,
                                       help='minimum percentage of the same amino acid required to retain column')
    optional_align.add_argument('--min_perc_taxa', type=float, default=50,
                                       help='minimum percentage of taxa required required to retain column')
    optional_align.add_argument('--prefix', required=False, default='gtdbtk',
                                       help='desired prefix for output files')
    optional_align.add_argument('--cpus', default=1, type=int,
                                    help='number of CPUs to use')
    optional_align.add_argument('-h', '--help', action="help",
                                       help="show help message")
                                       
    # infer tree
    infer_parser = subparsers.add_parser('infer', conflict_handler='resolve',
                                         formatter_class=CustomHelpFormatter,
                                         help='Infer tree from multiple sequence alignment.',)

    required_infer = infer_parser.add_argument_group('required named arguments')
    required_infer.add_argument('--msa_file', required=True,
                                    help="multiple sequence alignment in FASTA format")
    required_infer.add_argument('--out_dir', required=True,
                                    help='directory to output files')

    optional_infer = infer_parser.add_argument_group('optional arguments')
    optional_infer.add_argument('--prot_model', choices=['WAG', 'LG'], 
                                    help='protein substitution model for tree inference', default='WAG')
    optional_infer.add_argument('--prefix', required=False, default='gtdbtk',
                                    help='desired prefix for output files')
    optional_infer.add_argument('--cpus', default=1, type=int,
                                    help='number of CPUs to use')
    optional_infer.add_argument('-h', '--help', action="help",
                                    help="show help message")
                                       
    # root tree using outgroup
    root_parser = subparsers.add_parser('root', conflict_handler='resolve',
                                        formatter_class=CustomHelpFormatter,
                                        help='Root tree using an outgroup.',)

    required_root = root_parser.add_argument_group('required named arguments')
    required_root.add_argument('--input_tree', required=True,
                                help="tree to root in Newick format")
    required_root.add_argument('--outgroup_taxon', required=True,
                                help="taxon to use as outgroup (e.g., p__Patescibacteria)")
    required_root.add_argument('--output_tree', required=True,
                                help='output tree')

    optional_root = root_parser.add_argument_group('optional arguments')
    optional_root.add_argument('-h', '--help', action="help",
                                help="show help message")
                                       
    # decorate tree
    decorate_parser = subparsers.add_parser('decorate', conflict_handler='resolve',
                                                formatter_class=CustomHelpFormatter,
                                                help='Decorate tree with GTDB taxonomy.',)

    required_decorate = decorate_parser.add_argument_group('required named arguments')
    required_decorate.add_argument('--input_tree', required=True,
                                    help="tree to root in Newick format")
    required_decorate.add_argument('--output_tree', required=True,
                                    help='output tree')

    optional_decorate = decorate_parser.add_argument_group('optional arguments')
    optional_decorate.add_argument('-h', '--help', action="help",
                                    help="show help message")

    #-------------------------------------------------
    # get and check options
    args = None
    if(len(sys.argv) == 1):
        printHelp()
        sys.exit(0)
    elif(sys.argv[1] == '-v' or
         sys.argv[1] == '--v' or
         sys.argv[1] == '-version' or
         sys.argv[1] == '--version'):
        print "gtdbtk: version %s %s %s" % (__version__,
                                            __copyright__,
                                            __author__)
        sys.exit(0)
    elif(sys.argv[1] == '-h' or
         sys.argv[1] == '--h' or
         sys.argv[1] == '-help' or
         sys.argv[1] == '--help'):
        printHelp()
        sys.exit(0)
    else:
        args = parser.parse_args()
        
    # setup logger
    if hasattr(args, 'out_dir'):
        logger_setup(args.out_dir, "gtdb_tk.log", "GTDB-Tk", __version__, False)
    else:
        logger_setup(None, "gtdb_tk.log", "GTDB-Tk", __version__, False)

    #-------------------------------------------------
    # do what we came here to do
    try:
        gt_parser = gtdbtk.OptionsParser(__version__)
        if(False):
            import cProfile
            cProfile.run('gt_parser.parseOptions(args)', 'prof')
        else:
            gt_parser.parse_options(args)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
