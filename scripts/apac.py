#!/usr/bin/python
''' This script is for generating an APAC report'''

#
# Copyright (C) 2010, Susmit Shannigrahi, Susmit AT fedoraproject DOT org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import getpass
from fedora.client.fas2 import AccountSystem
import datetime

#from maxmind array
#changes are: 'RS': 'EU', 'ME': 'EU', 'AU': 'AS', 'NZ': 'AS'
#https://fedorahosted.org/fedora-infrastructure/ticket/2921
#changes are: 'IL': 'EU', 'KG': 'EU', 'LB': 'EU', 'SA': 'EU', 'AE': 'EU'


CONTINENT_MAP = {'AP': 'AS', 'EU': 'EU', 'AD': 'EU', 'AE': 'EU', 'AF': 'AS', \
                 'AG': 'SA', 'AI': 'SA', 'AL': 'EU', 'AM': 'AS', 'AN': 'SA', 'AO': 'AF', \
                 'AQ': 'AN', 'AR': 'SA', 'AS': 'OC', 'AT': 'EU', 'AU': 'OC', 'AW': 'SA', \
                 'AX': 'EU', 'AZ': 'AS', 'BA': 'EU', 'BB': 'SA', 'BD': 'AS', 'BE': 'EU', \
                 'BF': 'AF', 'BG': 'EU', 'BH': 'AS', 'BI': 'AF', 'BJ': 'AF', 'BM': 'SA', \
                 'BN': 'AS', 'BO': 'SA', 'BR': 'SA', 'BS': 'SA', 'BT': 'AS', 'BV': 'AF', \
                 'BW': 'AF', 'BY': 'EU', 'BZ': 'SA', 'CA': 'NA', 'CC': 'AS', 'CD': 'AF', \
                 'CF': 'AF', 'CG': 'AF', 'CH': 'EU', 'CI': 'AF', 'CK': 'OC', 'CL': 'SA', \
                 'CM': 'AF', 'CN': 'AS', 'CO': 'SA', 'CR': 'SA', 'CU': 'SA', 'CV': 'AF', \
                 'CX': 'AS', 'CY': 'AS', 'CZ': 'EU', 'DE': 'EU', 'DJ': 'AF', 'DK': 'EU', \
                 'DM': 'SA', 'DO': 'SA', 'DZ': 'AF', 'EC': 'SA', 'EE': 'EU', 'EG': 'AF', \
                 'EH': 'AF', 'ER': 'AF', 'ES': 'EU', 'ET': 'AF', 'FI': 'EU', 'FJ': 'OC', \
                 'FK': 'SA', 'FM': 'OC', 'FO': 'EU', 'FR': 'EU', 'FX': 'EU', 'GA': 'AF', \
                 'GB': 'EU', 'GD': 'SA', 'GE': 'AS', 'GF': 'SA', 'GG': 'EU', 'GH': 'AF', \
                 'GI': 'EU', 'GL': 'SA', 'GM': 'AF', 'GN': 'AF', 'GP': 'SA', 'GQ': 'AF', \
                 'GR': 'EU', 'GS': 'SA', 'GT': 'SA', 'GU': 'OC', 'GW': 'AF', 'GY': 'SA', \
                 'HK': 'AS', 'HM': 'AF', 'HN': 'SA', 'HR': 'EU', 'HT': 'SA', 'HU': 'EU', \
                 'ID': 'AS', 'IE': 'EU', 'IL': 'EU', 'IM': 'EU', 'IN': 'AS', 'IO': 'AS', \
                 'IQ': 'AS', 'IR': 'AS', 'IS': 'EU', 'IT': 'EU', 'JE': 'EU', 'JM': 'SA', \
                 'JO': 'AS', 'JP': 'AS', 'KE': 'AF', 'KG': 'EU', 'KH': 'AS', 'KI': 'OC', \
                 'KM': 'AF', 'KN': 'SA', 'KP': 'AS', 'KR': 'AS', 'KW': 'AS', 'KY': 'SA', \
                 'KZ': 'AS', 'LA': 'AS', 'LB': 'EU', 'LC': 'SA', 'LI': 'EU', 'LK': 'AS', \
                 'LR': 'AF', 'LS': 'AF', 'LT': 'EU', 'LU': 'EU', 'LV': 'EU', 'LY': 'AF', \
                 'MA': 'AF', 'MC': 'EU', 'MD': 'EU', 'MG': 'AF', 'MH': 'OC', 'MK': 'EU', \
                 'ML': 'AF', 'MM': 'AS', 'MN': 'AS', 'MO': 'AS', 'MP': 'OC', 'MQ': 'SA', \
                 'MR': 'AF', 'MS': 'SA', 'MT': 'EU', 'MU': 'AF', 'MV': 'AS', 'MW': 'AF', \
                 'MX': 'NA', 'MY': 'AS', 'MZ': 'AF', 'NA': 'AF', 'NC': 'OC', 'NE': 'AF', \
                 'NF': 'OC', 'NG': 'AF', 'NI': 'SA', 'NL': 'EU', 'NO': 'EU', 'NP': 'AS', \
                 'NR': 'OC', 'NU': 'OC', 'NZ': 'AS', 'OM': 'AS', 'PA': 'SA', 'PE': 'SA', \
                 'PF': 'OC', 'PG': 'OC', 'PH': 'AS', 'PK': 'AS', 'PL': 'EU', 'PM': 'SA', \
                 'PN': 'OC', 'PR': 'SA', 'PS': 'AS', 'PT': 'EU', 'PW': 'OC', 'PY': 'SA', \
                 'QA': 'AS', 'RE': 'AF', 'RO': 'EU', 'RU': 'EU', 'RW': 'AF', 'SA': 'AS', \
                 'SB': 'OC', 'SC': 'AF', 'SD': 'AF', 'SE': 'EU', 'SG': 'AS', 'SH': 'AF', \
                 'SI': 'EU', 'SJ': 'EU', 'SK': 'EU', 'SL': 'AF', 'SM': 'EU', 'SN': 'AF', \
                 'SO': 'AF', 'SR': 'SA', 'ST': 'AF', 'SV': 'SA', 'SY': 'AS', 'SZ': 'AF', \
                 'TC': 'SA', 'TD': 'AF', 'TF': 'AF', 'TG': 'AF', 'TH': 'AS', 'TJ': 'AS', \
                 'TK': 'OC', 'TM': 'AS', 'TN': 'AF', 'TO': 'OC', 'TP': 'AS', 'TR': 'EU', \
                 'TT': 'SA', 'TV': 'OC', 'TW': 'AS', 'TZ': 'AF', 'UA': 'EU', 'UG': 'AF', \
                 'UM': 'OC', 'US': 'NA', 'UY': 'SA', 'UZ': 'AS', 'VA': 'EU', 'VC': 'SA', \
                 'VE': 'SA', 'VG': 'SA', 'VI': 'SA', 'VN': 'AS', 'VU': 'OC', 'WF': 'OC', \
                 'WS': 'OC', 'YE': 'AS', 'YT': 'AF', 'YU': 'EU', 'ZA': 'AF', 'ZM': 'AF', \
                 'ZR': 'AF', 'ZW': 'AF', 'RS': 'EU', 'ME': 'EU', 'AU': 'AS'}

group_list = ['ambassadors','freemedia','designteam','docs',\
              'docs-publishers','docs-writers','fi-apprentice',\
              'freemedia','fedora-arm','l10n-commits','l10n-admin',\
              'l10n-editor','marketing','magazine','news','packager',\
              'provenpackager','proventesters','qa','sysadmin-accounts',\
              'sysasdmin-ask','sysadmin-badges','trigers','web',]

def calc_list():
    '''
    Calculate a list of APAC contributors in different teams
    '''

    output = []
    people_list = []
    country_list = []
    flag = 0
    final_output_list_as = [] 
    final_output_list_eu = []
    final_output_list_na = []
    final_output_list_latam = []
    final_output_list_africa = []
    final_output_list_unknown = []
    full_name = {'AS' : 'APAC', 'NA' : 'North America', \
'SA' : 'LATAM', 'AF' : 'Africa', 'EU' : 'EMEA', 'Unknown' : 'Unknown'}


#    username = 'fedoradummy'
#    password = '<%= fedoraDummyUserPassword %>'    
    username = raw_input('Username: ').strip()
    password = getpass.getpass('Password: ')    
    fas = AccountSystem(username=username, password=password)

    # Get a dictinary of all people in FAS
    data = fas.people_by_key(key='id', search=u'*', \
fields=['human_name', 'username', 'email', 'status', 'country_code'])

    # Get a list of people in the groups we care about
    for group_name in group_list:
        print "Group: %s" % group_name

        # Get the people from this group
        group_people = fas.group_members(group_name)
        #make a list of usernames of a group
        for person in group_people:

        # match our people list to all of FAS now
            for item in data.values():
                user_name = item['username']
                human_name = item['human_name']
                country_code = item['country_code']
                status = item['status']
                email = item['username'] + '@fedoraproject.org'

                if person == user_name:
                    if status == 'active': #filter out all inactive accounts
                        if country_code is None or country_code == 'O1' \
    or country_code == '  ':
                            continent_code = 'Unknown'            
                        else:
                            continent_code = CONTINENT_MAP[country_code]

                       #different values for blank or non-blank fields are
                       #_____________________________________________________#
                       # Country Code  || Human Name || Number of tickets||  #
                       #_____________________________________________________#
                       # None          || None/Name  ||  0/n                 #
                       # '   '         || None/Name  ||                      #
                       # 'IN','FR' etc.|| None/Name  ||                      #
                       #_____________________________________________________#

                        if country_code is None:
                            if human_name is None:
                                flag = 1
                            else:
                                flag = 2
                        elif country_code == '  ':
                            if human_name is None:
                                flag = 1
                            else:
                                flag = 2

                        else: #if there is a country code available
                            country = countries[country_code]
                            if human_name is None:
                                flag = 3
                            else:
                                flag = 4

                        #check flag to decide o/p
                        if flag == 1:
                            entry = [user_name, user_name, 'Unknown', email, \
    'Unknown']
                            output.append(entry)
                        elif flag == 2:
                            entry = [user_name, human_name, 'Unknown', email, \
    'Unknown']
                            output.append(entry)
                        elif flag == 3:
                            entry = [user_name, user_name, country, email, \
    continent_code]
                            output.append(entry)
                        else:
                            entry = [user_name, human_name, country, email, \
    continent_code]
                            output.append(entry)

# Now we have a output list like 
#[['rdsharma4u', 'Ravi Datta Sharma','India','rdsharma4u@gmail.com','1','AS'],
#['red', 'Sandro Mathys', 'Switzerland', 'sm@sandro-mathys.ch', '10', 'EU']]

    for item in output:
        #break
        continent_code = item[4]
        if continent_code == 'AS' or continent_code == 'AU':
            final_output_list_as.append(item)
        elif continent_code == 'NA':
            final_output_list_na.append(item)
        elif continent_code == 'SA':
            final_output_list_latam.append(item)
        elif continent_code == 'EU':
            final_output_list_eu.append(item)
        elif continent_code == 'AF':
            final_output_list_africa.append(item)
        elif continent_code == 'Unknown':
            final_output_list_unknown.append(item)

    print final_output_list_as

if __name__ == "__main__":
    calc_list()

