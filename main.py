import formatText
import functions
import checkSpecial
import os 
import constant
from flask import Flask,render_template , request ,flash,redirect,send_file
from werkzeug.utils import secure_filename
import shutil 
from pathlib import Path

app = Flask(__name__)
UPLOAD_FOLDER = './pdf-uploads'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 512  * 1024 * 1024
ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def tot():
    text = functions.readPdf('0000550176538_005500634163.pdf')
    text = functions.checkUTF8(text)
    listData = functions.removeWhiteSpace(text)
    listData = functions.cleanData2(listData)
    listType = functions.checkType2(listData)
    listData,listType = checkSpecial.tot(listData,listType) 
    result = formatText.formatCdr(listData,listType,'TOT')
    print("print")
    functions.exportText(result,"cdr1000PAGE")
    resultInv = formatText.formatInventory(listData,listType,'TOT')
    functions.exportText(resultInv,"inven1000PAGE")
    print(len(listData))
    print(len(listType))

def ais(fullpath,filename,isCdr):
    text = functions.readPdf(fullpath) #W-IN-11-6211-0261858-2.pdf

    # text = checkUTF8(text)
    listData = functions.removeWhiteSpace(text)
    listData = functions.cleanData2(listData)
    listData = functions.changeword(listData)
    listData = functions.cleanDataAis(listData)
    listData = functions.wordCheck(listData)
    listType = functions.checkType2(listData)
 
 
    # functions.exportText(listData,"result/"+filename+"-text.txt")
    listData,listType = checkSpecial.ais(listData,listType) 

    result , resultInternet = formatText.formatUsage(listData,listType,filename,'AIS')

    if isCdr :
        result = formatText.formatCdr(listData,listType,filename,'AIS')
        functions.exportText(result,"result/cdr/"+filename+"-CDR.txt")
    else:
        functions.exportText(result,"result/usage/"+filename+"-USAGE.txt")
        functions.exportText(resultInternet,"result/usage-internet/"+filename+"-USAGE-INTERNET.txt")

        result = formatText.formatInventory(listData,listType,filename,'AIS')
        functions.exportText(result,"result/inventory/"+filename+"-INVENTORY.txt")

        result = formatText.formatPromotion(listData,listType,filename,'AIS')
        functions.exportText(result,"result/promotion/"+filename+"-PROMOTION.txt")

    print(len(listData))
    print(len(listType))
    functions.deleteFile(fullpath)

def dtac():
    text = functions.readPdf('Invoice.pdf') #W-IN-11-6211-0261858-2.pdf
    listData = functions.removeWhiteSpace(text)
    # functions.exportText(text,"Dtac-Invoice.txt")

def true(fullpath,filename):
    text = functions.readPdf(fullpath)
    text = functions.checkUTF8(text)
    listData = functions.removeWhiteSpace(text)
    listData = functions.wordCheck(listData)
    listType = functions.checkType2(listData)
    
    listData,listType = checkSpecial.true(listData,listType) 

    result = formatText.formatPromotion(listData,listType,filename,'TRUE')
    functions.exportText(result,"result/promotion/"+filename+"-PROMOTION.txt")

    result = formatText.formatGetPackage(listData,listType,filename,'TRUE')
    functions.exportText(result,"result/get-package/"+filename+"-GETPACKAGE.txt")
    functions.deleteFile(fullpath)



@app.route("/upload-pdf")
def index():  #def  เป็นคำสำคัญสำหรับการสร้างฟังก์ชัน
   return render_template("index.html") #เรนเดอร์ไฟล์ที่ชื่อ index ที่อยู่ในไดเร้กทอรี่ที่ชื่อ templates


@app.route('/uploads', methods=['POST'])
def upload_file():
    cdrAis = False
    if request.method == 'POST':
        opr = request.form['options']

        if request.form.get('cdr-ais'):
            cdrAis = True

        if 'files[]' not in request.files:
            flash("No file part")
            return redirect(request.url)
        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File(s) successfully uploaded')


        project_root = constant.PROJECTROOT
        project_root = os.path.join(project_root, 'app')
        # project_root = os.path.join(project_root, 'pythonBluecode')
        project_root_result = os.path.join(project_root, 'result')

        usage_path = os.path.join(project_root_result, 'usage')
        functions.deleteFileListDir(usage_path)
        usage_internet_path = os.path.join(project_root_result, 'usage-internet')
        functions.deleteFileListDir(usage_internet_path)
        promotion_path = os.path.join(project_root_result, 'promotion')
        functions.deleteFileListDir(promotion_path)
        inventory_path = os.path.join(project_root_result, 'inventory')
        functions.deleteFileListDir(inventory_path)
        get_package_path  = os.path.join(project_root_result, 'get-package')
        functions.deleteFileListDir(get_package_path)
        get_cdr_path  = os.path.join(project_root_result, 'cdr')
        functions.deleteFileListDir(get_cdr_path)

        output_path = os.path.join(project_root, 'pdf-uploads')
        directory = os.fsencode(output_path)

        Path(usage_path).mkdir(parents=True, exist_ok=True)
        Path(usage_internet_path).mkdir(parents=True, exist_ok=True)
        Path(promotion_path).mkdir(parents=True, exist_ok=True)
        Path(inventory_path).mkdir(parents=True, exist_ok=True)
        Path(get_package_path).mkdir(parents=True, exist_ok=True)
        Path(get_cdr_path).mkdir(parents=True, exist_ok=True)
       
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            fullpath = output_path+"\\"+filename    
            filename = filename.split(".")
            if filename[1] == "pdf":
                if opr in "ais":
                    ais(fullpath,filename[0],cdrAis)
                elif opr in "true":
                    true(fullpath,filename[0])
                elif opr in "dtac":
                    dtac() #wait dev

        shutil.make_archive('result-archive', 'zip', project_root_result)
        
    # 
    # return redirect('/upload-pdf')
    return send_file(project_root+'/result-archive.zip', attachment_filename='result-archive.zip')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)