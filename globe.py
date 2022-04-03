##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2022.04.03
## Description:    Global variables
## Notes:
##  - Colours are represented as either the ANSI colour number, OR the full ANSI escape sequence
import os
#-------------------#
#    Environment    #
#-------------------#
LABEL_FILE="./ip.labels"  #File that holds all the ip labels
LABEL_COLOUR="1;45"  #Bold;Purple | Follows ANSI code

#------------#
#    Grid    #
#------------#
UNIT_SIZE=9  #Do not touch!
can_draw=True  #Tells the listener it's allowed to draw on the screen
toggle_labels=True  #Do not touch!

#---------------#
#    Network    #
#---------------#
#This is a list of CIDR subnet masks to compare IPs with
#Try to keep these in descending order
SUBNETS=[24,21,20,16]

#-------------------#
#    IP Matching    #
#-------------------#
ip_colour=3  #1-6
subnet_colour=2  #1-6; Start with yellow cuz it looks nicer
