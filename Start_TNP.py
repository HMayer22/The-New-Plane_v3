from flask import Flask, render_template, request, Response
from waitress import serve
import TNP

logo = TNP.logo()
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        
        global settings, domain
        domain = request.form.get('domain')
        port = request.form.get('port') if request.form.get('port') != '' else "Default"
        options = request.form.get('options')
        threads = request.form.get('threads') if request.form.get('threads') != '' else "2500"
        methods = request.form.get('methods')
        tdthreads, tdmethod = "Threads", "Method"
        settings = {'scan': True if options == "SCAN" else False,
                'method': methods,
                'attackhttp': True if options == "HTTP" else False,
                'attackhttps': True if options == "HTTPS" else False,
                'threads': None if request.form.get('threads') == '' else int(request.form.get('threads')),
                'port': None if request.form.get('port') == '' else int(request.form.get('port'))}
        
        if options == "SCAN":
            tdthreads = tdmethod = methods = threads = ""
        
        data = (domain, port, options, tdthreads, threads, tdmethod, methods)
        
        return render_template('response.html', entries=data)
    
    return render_template('index.html')

@app.route('/stream')
def stream():
    TNP.stopcreate()
    
    def event_stream():
        output_main = TNP.main(domain, settings)
        
        for text_main in output_main:
            yield f"data: {text_main}\n\n"

    return Response(event_stream(), content_type='text/event-stream')

@app.route('/stop', methods=['POST'])
def stop_attack():
    return TNP.stopcode()

def main():
    ip, port = "127.0.0.1", 1109
    
    print(f"""
          {logo}
          \033[95mTNP running on http://{ip if ip != '0.0.0.0' else '127.0.0.1'}:{port}/\033[0m
          {"(Press CTRL+C to stop)":^35}\r\n""")
    
    serve(app, host=ip, port=port)

if __name__ == '__main__':
    main()
