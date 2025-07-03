from flask import Flask, render_template, request, send_file, jsonify
from fpdf import FPDF
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/export', methods=['POST'])
def export_pdf():
    data = request.get_json()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'MATEO - Marco L\xf3gico', ln=True, align='C')
    pdf.ln(5)
    objectives = data.get('objectives', [])
    for obj in objectives:
        pdf.set_font('Arial', 'B', 14)
        pdf.multi_cell(0, 10, f"Objetivo: {obj.get('description','')}")
        results = obj.get('results', [])
        for res in results:
            pdf.set_font('Arial', 'B', 12)
            pdf.multi_cell(0, 8, f"Resultado: {res.get('description','')}")
            pdf.set_font('Arial', '', 11)
            for ind in res.get('indicators', []):
                desc = ind.get('description','')
                means = ind.get('means','')
                pdf.multi_cell(0, 6, f"- Indicador: {desc}\n  Medio: {means}")
            for act in res.get('activities', []):
                desc = act.get('description','')
                means = act.get('means','')
                pdf.multi_cell(0, 6, f"- Actividad: {desc}\n  Medio: {means}")
            pdf.ln(2)
        pdf.ln(2)
    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='marco_logico.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
