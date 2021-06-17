raw_database = [    
                    "(BUS B1)",
                    "(ATIME B1 HUE 19:00HR)",
                    "(DTIME B1 HCMC 10:00HR)",
                    "(RUN-TIME B1 HCMC HUE 9:00HR)",
                    "(BUS B2)",
                    "(ATIME B2 HUE 22:30HR)",
                    "(DTIME B2 HCMC 14:30HR)",
                    "(RUN-TIME B2 HCMC HUE 8:00HR)",
                    "(BUS B3)",
                    "(ATIME B3 HUE 20:00HR)",
                    "(DTIME B3 DANANG 16:00HR)",
                    "(RUN-TIME B3 DANANG HUE 4:00HR)",
                    "(BUS B4)",
                    "(ATIME B4 HCMC 18:30HR)",
                    "(DTIME B4 DANANG 8:30HR)",
                    "(RUN-TIME B4 DANANG HCMC 10:00HR)",
                    "(BUS B5)",
                    "(ATIME B5 HN 23:30HR)",
                    "(DTIME B5 DANANG 5:30HR)",
                    "(RUN-TIME B5 DANANG HN 18:00HR)",
                    "(BUS B6)",
                    "(ATIME B6 HN 22:30HR)",
                    "(DTIME B6 HUE 6:30HR)",
                    "(RUN-TIME B6 HUE HN 16:00HR)",
                ]




def write_file(output_file,content):
    with open(output_file+".txt","w+",encoding="utf-8")as f:
        f.write(content)


def categorize_database(database):
    """
    Categorize raw database to collections of bus, ATIME and DTIME
    ----------------------------------------------------------------
    Args:
        database: raw database from assignments (List of string values)
    """
    #Remove ( )
    buss = [data.replace('(','').replace(')','') for data in database if 'BUS' in data]
    arrival_times = [data.replace('(','').replace(')','') for data in database if 'ATIME' in data]
    departure_times = [data.replace('(','').replace(')','') for data in database if 'DTIME' in data]
    run_times=[data.replace('(','').replace(')','') for data in database if 'RUN-TIME' in data]
    
    return {'bus': buss, 
            'arrival':arrival_times, 
            'departure':departure_times,
            'runtime':run_times}

def read_file(file_name):
    with open(file_name,"r",encoding='utf-8') as f:
        content = f.read()
        return content


