import json
        

def load(filename):
    """Takes a .json file as argument and returns a list sorted by 'project_id'. Only works with list filled with dictionaries. If no file is found None is returned."""
    try:
        with open(filename, "r") as fread:
            loaded = json.load(fread)
            #Sorts the database by the 'project_id' key in each dict object.
            loaded = sorted(loaded, key=lambda proj: proj["project_id"])
            return loaded
    except Exception as err:
        #If we get an error we assume that it was because of an incorrect filename. We return a better error message than stock.
        print("Kunde inte läsa in filen: " + filename)
        print("Felet var: " + str(err))
        return None



def get_project_count(li):
    """Takes a list of projects and returns the amount of projects in that list."""
    return len(li)



def get_project(li, project_id):
    """Takes a list and a project ID as arguments and returns the whole project dict that is related to the ID. If no match is found None is returned."""
    for project in li:
        if str(project["project_id"]) == str(project_id):
            return project
    else:
        return None



def search(li, sort_by ="start_date", sort_order ="desc", techniques =None, search =None, search_fields =None):
    """Returns a list only containing projects that match all given parameters through arguments. If no matches are found returns an empty list."""
    s_li = li.copy()

    #If nothing has been fed to search we simply do not run the search section of the code. Nothing get filtraded out.
    if search != None:
        #If the user has not specified any search fields we use the ones we see fit to search in. Image names and links that might be in a project should not make it appear in a search since they are not visible to the user.
        if search_fields == None:
            search_fields = ["project_id", "project_name", "start_date", "end_date", "course_id", "course_name", "short_description", "long_description", "group_size", "academic_credits", "techniques_used"]
        i = 0
        len_li = len(s_li)
        #Compare value of every field that has been specified to the string in search. If search does not appear in any of the values the project is deleted from the list.
        while i < len_li:
            for field in search_fields:
                # Hela den delen är för att hitta techniques_used om man skriver på sökfältet. Så den if satsen är specifikt för att gå djubare alltså i listan på techniques_used.
                if isinstance(field, list):
                    for tech in field:
                        cur_field = str(s_li[i][field][tech]).lower()
                        if search.lower() in cur_field:
                            i += 1
                            break
                # Den delen som täcker allt annat som inte är lista alltså techniques_used.       
                else:
                    cur_field = str(s_li[i][field]).lower()
                    if search.lower() in cur_field:
                        i += 1
                        break
            else:
                del s_li[i]
                len_li -= 1

    # If the user has not specified any techniques we skip this block. Otherwise all projects that does not match every technique that has been specified are deleted from the list.
    if techniques != None and techniques != []:
        i = 0
        len_li = len(s_li)
        while i < len_li:
            for tech in techniques:
                if tech not in s_li[i]["techniques_used"]:
                    del s_li[i]
                    len_li -= 1
                    break
            else:
                i += 1
            
    # Set reverse depending on user input.
    # Den delen är bara för asc och desc
    reverse = True
    if sort_order == "asc":
        reverse = False
    # The list is sorted using sort_by and reverse.
    s_li = sorted(s_li, key=lambda proj: proj[sort_by], reverse=reverse)
    return s_li


def get_techniques(li):
    """Takes a list and returns a list with 1 of every technique used in any project"""
    tech_li = []
    for proj in li:
        for tech in proj["techniques_used"]:
            tech_li.append(tech)
    # We sort the list alphabetically and remove any double occurences using sorted and set.
    tech_li = sorted(set(tech_li))
    return tech_li


## Den använder vi alldrig (Överflödig)
def get_technique_stats(li):
    """Takes a list and returns a list with unique techniques used in projects as keys and all projects where that technique is used as values for each key."""
    tech_stats = {}
    techs = get_techniques(li)
    for tech in techs:
        tech_stats[tech] = 0

    #Extracts certain data from each project that use a technique.
    for tech in tech_stats:
        projects = search(li, "project_id", "asc", [tech])
        rel_proj = []
        for proj in projects:
            info = {"id": proj["project_id"], "name" : proj["project_name"]}
            rel_proj.append(info)
        tech_stats[tech] = rel_proj

    return tech_stats
