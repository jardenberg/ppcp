"""One-off public reference-server reachability probe. No credentials or private inputs."""
import json
import socket
import urllib.error
import urllib.request
from datetime import datetime, timezone

VERSION = '0.1.0'
ORIGIN = 'https://joakim.jardenberg.net'


def fetch(path, user_agent, body=None):
    headers={'User-Agent':user_agent,'Accept':'text/html' if body is None else 'application/json, text/event-stream'}
    if body is not None:
        headers.update({'Content-Type':'application/json','MCP-Protocol-Version':'2025-11-25'})
        body=json.dumps(body).encode()
    try:
        r=urllib.request.urlopen(urllib.request.Request(ORIGIN+path,data=body,headers=headers),timeout=30)
    except urllib.error.HTTPError as error:
        r=error
    except Exception as error:
        return {'path':path,'error':str(error)}
    with r:
        data=r.read();text=data.decode('utf-8','replace')
        result={'path':path,'status':r.status,'bytes':len(data),'content_type':r.headers.get('Content-Type'),'profile_text_present':'Stacked Principles' in text and 'Katarina' in text}
        if r.status>=400:result['hosting_error_1010']='1010' in text
        if body is not None:
            try:
                frame=json.loads(data);value=frame.get('result',{})
                result.update({'rpc_error':frame.get('error',{}).get('code'),'protocol_version':value.get('protocolVersion'),'tools':[t['name'] for t in value.get('tools',[])],'working_section_returned':value.get('structuredContent',{}).get('section',{}).get('id')=='working-with-me-in-practice','signature_present':bool(value.get('_meta',{}).get('org.jardenberg/verifiable-mcp',{}).get('jws'))})
            except (ValueError,TypeError):result['not_json_rpc']=True
        return result


def main():
    report={'probe_version':VERSION,'checked_at':datetime.now(timezone.utc).isoformat(),'origin':ORIGIN,'limits':['Tests HTTP and MCP from this runner only; not a Google/Bing crawl or an indexing test.','User-Agent values are emulated.','Signature presence is reported, not cryptographically verified by this probe.']}
    try:report['dns_addresses']=sorted({r[4][0] for r in socket.getaddrinfo('joakim.jardenberg.net',443)})
    except Exception as error:report['dns_error']=str(error)
    report['clients']={name:fetch('/',agent) for name,agent in [('named','PPCP-reference-access-probe/0.1.0'),('urllib','Python-urllib/3.11'),('bingbot_emulation','Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)')]}
    agent='PPCP-reference-access-probe/0.1.0'
    report['markdown']=fetch('/profile.md',agent)
    report['initialize']=fetch('/mcp',agent,{'jsonrpc':'2.0','id':0,'method':'initialize','params':{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'PPCP-access-probe','version':VERSION}}})
    report['initialized_notification']=fetch('/mcp',agent,{'jsonrpc':'2.0','method':'notifications/initialized'})
    report['tools']=fetch('/mcp',agent,{'jsonrpc':'2.0','id':1,'method':'tools/list','params':{}})
    report['retrieval']=fetch('/mcp',agent,{'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'ppcp_get_section','arguments':{'section_id':'working-with-me-in-practice'}}})
    report['required_checks_passed']=bool(report.get('dns_addresses')) and report['clients']['named'].get('profile_text_present',False) and report['markdown'].get('profile_text_present',False) and report['initialize'].get('protocol_version')=='2025-11-25' and report['initialized_notification'].get('status')==202 and len(report['tools'].get('tools',[]))==6 and report['retrieval'].get('working_section_returned',False)
    report['all_tested_clients_passed']=all(x.get('status')==200 and x.get('profile_text_present') for x in report['clients'].values())
    print(json.dumps(report,indent=2))
    with open('reference-access-result.json','w') as f:json.dump(report,f,indent=2)
    if not report['all_tested_clients_passed']:
        print('::warning::Some tested clients could not retrieve the public profile. See the client-specific results; this is not universal access.')
    return 0 if report['required_checks_passed'] else 1


if __name__=='__main__':raise SystemExit(main())
