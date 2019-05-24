from jenkinsapi.jenkins import Jenkins


def get_server_instance():
    jenkins_url = 'http://jenkins.yuminsoft.local/jenkins/'
    server = Jenkins(jenkins_url, username='YM10074', password='Alan666')
    return server

"""Get job details of each job that is running on the Jenkins instance"""
def get_job_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for job_name, job_instance in server.get_jobs():
        print('Job Name:%s' % (job_instance.name))
        print('Job Description:%s' % (job_instance.get_description()))
        print('Is Job running:%s' % (job_instance.is_running()))
        print('Is Job enabled:%s' % (job_instance.is_enabled()))

def getSCMInfroFromLatestGoodBuild(jobName):
    server = get_server_instance()
    job = server[jobName]
    lgb = job.get_last_good_build()
    return lgb.get_revision()

def get_plugin_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for plugin in server.get_plugins().values():
        print("Short Name:%s" % (plugin.shortName))
        print("Long Name:%s" % (plugin.longName))
        print("Version:%s" % (plugin.version))
        print("URL:%s" % (plugin.url))
        print("Active:%s" % (plugin.active))
        print("Enabled:%s" % (plugin.enabled))

if __name__ == '__main__':
    print(get_job_details())