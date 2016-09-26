"""This dict is used in `haproxy.py` to build the redirects that are not on the
cluster.
"""

REDIRECTS = [
    {
        'from': '/',
        'to': 'http://labs.icahn.mssm.edu/maayanlab/'
    },
    {
        'from': '/l1kdownload/',
        'to': 'http://10.91.53.225/CD/'
    },
    {
        'from': '/lachmann/upload',
        'to': 'http://ATP:8080/lachmann/upload'
    },
    {
        'from': '/Excel2BiositemapsAndHTML',
        'to': 'http://vn1.pharm.mssm.edu/Excel2BiositemapsAndHTML'
    },
    {
        'from': '/iscmid',
        'to': 'http://vn1.pharm.mssm.edu/iscmid'
    },
    {
        'from': '/datasets',
        'to': 'http://vn1.pharm.mssm.edu/datasets'
    },
    {
        'from': '/genes2fans',
        'to': 'http://vn1.pharm.mssm.edu/genes2fans'
    },
    {
        'from': '/result/kea',
        'to': 'http://vn1.pharm.mssm.edu/result/kea'
    },
    {
        'from': '/lib',
        'to': 'http://vn1.pharm.mssm.edu/lib'
    },
    {
        'from': '/genes2networks',
        'to': 'http://vn1.pharm.mssm.edu/genes2networks'
    },
    {
        'from': '/presynaptome',
        'to': 'http://vn1.pharm.mssm.edu/presynaptome'
    },
    {
        'from': '/l2n',
        'to': 'http://vn1.pharm.mssm.edu/l2n'
    },
    {
        'from': '/library',
        'to': 'http://vn1.pharm.mssm.edu/library'
    },
    {
        'from': '/chea',
        'to': 'http://vn1.pharm.mssm.edu/chea'
    },
    {
        'from': '/maayan-lab',
        'to': 'http://vn1.pharm.mssm.edu/maayan-lab'
    },
    {
        'from': '/ESCAPE',
        'to': 'http://vn1.pharm.mssm.edu/ESCAPE'
    },
    {
        'from': '/lib/chea.jsp',
        'to': 'http://amp.pharm.mssm.edu/ChEA2/'
    },
    {
        'from': '/lib/kea.jsp',
        'to': 'http://www.maayanlab.net/KEA2/'
    },
    {
        'from': '/baylor',
        'to': 'http://amp.pharm.mssm.edu/bcm-idg/'
    }
]
