from flask import Flask,render_template,redirect,request,session,send_file
from web3 import Web3,HTTPProvider
import json
import qrcode
from io import BytesIO

def connect_with_register(acc):

    web3=Web3(HTTPProvider('http://127.0.0.1:7545'))
    if acc==0:
        web3.eth.defaultAccount=web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=acc
    
    artifact_path='./build/contracts/register.json'
    with open(artifact_path) as f:
        artifact_json=json.load(f)
        contract_abi=artifact_json['abi']
        contract_address=artifact_json['networks']['5777']['address']
    
    contract=web3.eth.contract(abi=contract_abi,address=contract_address)
    return contract,web3

app=Flask(__name__)
app.secret_key='1234'

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/loginManufacturer',methods=['post','get'])
def loginManufacturer():
    manufacturerWallet=request.form['manufacturerWallet']
    password=request.form['password']
    print(manufacturerWallet,password)
    contract,web3=connect_with_register(0)
    manufacturer,manuPassword=contract.functions.viewManufacturer().call()
    if manufacturer==manufacturerWallet and password==manuPassword:
        session['username']=manufacturer
        return redirect('/dashboard')
    return render_template('index.html',err='login invalid')

@app.route('/distributorForm',methods=['post'])
def distributorForm():
    distributorId=int(request.form['distributorId'])
    distributorName=request.form['distributorName']
    contactInfo=request.form['contactInfo']
    address=request.form['address']
    email=request.form['email']
    phone=request.form['phone']
    tin=request.form['tin']
    brn=request.form['brn']
    wallet=request.form['wallet']
    emergencycontact=request.form['emergencycontact']
    password=request.form['password']
    print(distributorId,distributorName,contactInfo,address,email,phone,tin,brn,wallet,emergencycontact,password)
    contract,web3=connect_with_register(0)
    tx_hash=contract.functions.addDistributor(distributorId,distributorName,contactInfo,address,email,phone,tin,brn,wallet,emergencycontact,password).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('distributors.html',res='Distributor Added')

@app.route('/supplierForm',methods=['post'])
def supplierForm():
    supplierId=int(request.form['supplierId'])
    supplierName=request.form['supplierName']
    contactInfo=request.form['contactInfo']
    address=request.form['address']
    email=request.form['email']
    phone=request.form['phone']
    tin=request.form['tin']
    brn=request.form['brn']
    wallet=request.form['wallet']
    emergencycontact=request.form['emergencycontact']
    password=request.form['password']
    print(supplierId,supplierName,contactInfo,address,email,phone,tin,brn,wallet,emergencycontact,password)
    contract,web3=connect_with_register(0)
    tx_hash=contract.functions.addSupplier(supplierId,supplierName,contactInfo,address,email,phone,tin,brn,wallet,emergencycontact,password).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('suppliers.html',res='Supplier Added')

@app.route('/productForm' ,methods=['post'])
def productForm():
    productId=request.form['productId']
    productName=request.form['productName']
    manufactureInfo=request.form['manufacturerInfo']
    lotNumber=request.form['lotNumber']
    manufacturingDate=request.form['manufacturingDate']
    expirationDate=request.form['expirationDate']
    serialNumber=request.form['serialNumber']
    uid=request.form['uid']
    print(productId,productName,manufactureInfo,lotNumber,manufacturingDate,expirationDate,serialNumber,uid)
    try:
        contract,web3=connect_with_register(0)
        tx_hash=contract.functions.addProduct(productId,productName,manufactureInfo,lotNumber,manufacturingDate,expirationDate,serialNumber,uid).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        qr = qrcode.make(productId)
        img = BytesIO()
        qr.save(img, 'PNG')
        img.seek(0)
    
        # Save QR code as a file
        filename = 'src/static/qrcodes/'+ productId+'.png'
        qr.save(filename)
    
        return render_template('products.html',res='Product Added')
    except:
        return render_template('products.html',err='Product already added')

@app.route('/dashboard')
def dashboardPage():
    return render_template('distributors.html')

@app.route('/ddashboard')
def ddashboardPage():
    return render_template('suppliers.html')

@app.route('/distributorslist')
def distributorslist():
    contract,web3=connect_with_register(0)
    _dids,_dnames,_dcontacts,_daddress,_demails,_dphones,_dtins,_dbrns,_dwallets,_demergency,_dpasswords=contract.functions.viewDistributors().call()
    data=[]
    for i in range(len(_dids)):
        dummy=[]
        dummy.append(_dids[i])
        dummy.append(_dnames[i])
        dummy.append(_dcontacts[i])
        dummy.append(_daddress[i])
        dummy.append(_demails[i])
        dummy.append(_dphones[i])
        dummy.append(_dtins[i])
        dummy.append(_dbrns[i])
        dummy.append(_dwallets[i])
        dummy.append(_demergency[i])
        data.append(dummy)
    return render_template('distributorslist.html',l=len(data),dashboard_data=data)

@app.route('/supplierslist')
def suppliersList():
    contract,web3=connect_with_register(0)
    _sids,_snames,_scontacts,_saddress,_semails,_sphones,_stins,_sbrns,_swallets,_semergency,_spasswords=contract.functions.viewSuppliers().call()
    data=[]
    for i in range(len(_sids)):
        dummy=[]
        dummy.append(_sids[i])
        dummy.append(_snames[i])
        dummy.append(_scontacts[i])
        dummy.append(_saddress[i])
        dummy.append(_semails[i])
        dummy.append(_sphones[i])
        dummy.append(_stins[i])
        dummy.append(_sbrns[i])
        dummy.append(_swallets[i])
        dummy.append(_semergency[i])
        data.append(dummy)
    return render_template('supplierslist.html',l=len(data),dashboard_data=data)

@app.route('/productslist')
def productslist():
    contract,web3=connect_with_register(0)
    _productId,_productName,_manufacturerInfo,_lotNumber,_manufacturingDate,_expirationDate,_serialNumber,_uid,_productstatus=contract.functions.viewProducts().call()

    data=[]
    for i in range(len(_productId)):
        dummy=[]
        dummy.append(_productId[i])
        dummy.append(_productName[i])
        dummy.append(_manufacturerInfo[i])
        dummy.append(_lotNumber[i])
        dummy.append(_manufacturingDate[i])
        dummy.append(_expirationDate[i])
        dummy.append(_serialNumber[i])
        dummy.append(_uid[i])
        if(_productstatus[i]==0):
            dummy.append('Not Distributed')
        elif(_productstatus[i]==1):
            dummy.append('Distributed')
        elif(_productstatus[i]==2):
            dummy.append('Supplied')
        data.append(dummy)
    return render_template('productslist.html',l=len(data),dashboard_data=data)

@app.route('/distributedproducts')
def distributedproducts():
    contract,web3=connect_with_register(0)
    _tdistributor,_tproduct=contract.functions.viewDistribution().call()
    _dids,_dnames,_dcontacts,_daddress,_demails,_dphones,_dtins,_dbrns,_dwallets,_demergency,_dpasswords=contract.functions.viewDistributors().call()
    _productId,_productName,_manufacturerInfo,_lotNumber,_manufacturingDate,_expirationDate,_serialNumber,_uid,_productstatus=contract.functions.viewProducts().call()
    data=[]
    for i in range(len(_tdistributor)):
        print(_dids,_tdistributor)
        dindex=_dids.index(int(_tdistributor[i]))
        dwallet=_dwallets[dindex]
        if dwallet==session['username']:
            dummy=[]
            pindex=_productId.index(_tproduct[i])
            dummy.append(_productId[pindex])
            dummy.append(_productName[pindex])
            dummy.append(_manufacturerInfo[pindex])
            dummy.append(_lotNumber[pindex])
            dummy.append(_manufacturingDate[pindex])
            dummy.append(_expirationDate[pindex])
            dummy.append(_serialNumber[pindex])
            dummy.append(_uid[pindex])
            if _productstatus[pindex]==1:
                dummy.append('Available to Supply')
            elif _productstatus[pindex]==2:
                dummy.append('Supplied')
            data.append(dummy)

    return render_template('myproducts.html',l=len(data),dashboard_data=data)

@app.route('/sendtosupplier')
def sendtosupplier():
    contract,web3=connect_with_register(0)
    _dids,_dnames,_dcontacts,_daddress,_demails,_dphones,_dtins,_dbrns,_dwallets,_demergency,_dpasswords=contract.functions.viewDistributors().call()
    _sids,_snames,_scontacts,_saddress,_semails,_sphones,_stins,_sbrns,_swallets,_semergency,_spasswords=contract.functions.viewSuppliers().call()
    _tdistributor,_tproduct=contract.functions.viewDistribution().call()
    _productId,_productName,_manufacturerInfo,_lotNumber,_manufacturingDate,_expirationDate,_serialNumber,_uid,_productstatus=contract.functions.viewProducts().call()
    data1=[]
    for i in range(len(_tdistributor)):
        print(_dids,_tdistributor)
        dindex=_dids.index(int(_tdistributor[i]))
        dwallet=_dwallets[dindex]
        print(dwallet)
        if dwallet==session['username']:
            pindex=_productId.index(_tproduct[i])
            if _productstatus[pindex]==1:
                dummy=[]
                dummy.append(_productId[pindex])
                dummy.append(_productName[pindex])
                data1.append(dummy)
                print(data1)

    data2=[]
    _sids,_snames,_scontacts,_saddress,_semails,_sphones,_stins,_sbrns,_swallets,_semergency,_spasswords=contract.functions.viewSuppliers().call()
    for i in range(len(_sids)):
        dummy=[]
        dummy.append(_sids[i])
        dummy.append(_snames[i])
        data2.append(dummy)
    return render_template('sendtosupplier.html',l1=len(data1),l2=len(data2),dashboard_data1=data1,dashboard_data2=data2)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/saboutus')
def saboutus():
    return render_template('aboutus1.html')

@app.route('/logout')
def logout():
    session['username']=None
    return redirect('/')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/loginDistributor',methods=['post'])
def loginDistributor():
    distributorWallet=request.form['distributorWallet']
    password=request.form['password1']
    print(distributorWallet,password)
    contract,web3=connect_with_register(0)
    _dids,_dnames,_dcontacts,_daddress,_demails,_dphones,_dtins,_dbrns,_dwallets,_demergency,_dpasswords=contract.functions.viewDistributors().call()
    for i in range(len(_dids)):
        print(_dwallets,_dpasswords)
        if(_dwallets[i]==distributorWallet and password==_dpasswords[i]):
            session['username']=distributorWallet
            return redirect('/ddashboard')
    return render_template('index.html',err='login invalid')

@app.route('/sendtodistributor')
def sendtodistributor():
    contract,web3=connect_with_register(0)
    _dids,_dnames,_dcontacts,_daddress,_demails,_dphones,_dtins,_dbrns,_dwallets,_demergency,_dpasswords=contract.functions.viewDistributors().call()
    data1=[]
    for i in range(len(_dids)):
        dummy=[]
        dummy.append(_dids[i])
        dummy.append(_dnames[i])    
        data1.append(dummy)
    data2=[]
    _productId,_productName,_manufacturerInfo,_lotNumber,_manufacturingDate,_expirationDate,_serialNumber,_uid,_productstatus=contract.functions.viewProducts().call()
    for i in range(len(_productId)):
        if(_productstatus[i]==0):
            dummy=[]
            dummy.append(_productId[i])
            dummy.append(_productName[i])
            data2.append(dummy)
    return render_template('sendtodistributor.html',l1=len(data1),l2=len(data2),dashboard_data1=data1,dashboard_data2=data2)

@app.route('/sendtosupplierform',methods=['post'])
def sendtosupplyform():
    productid=request.form['productid']
    supplierid=request.form['supplierid']
    print(productid,supplierid)
    contract,web3=connect_with_register(0)
    tx_hash=contract.functions.sendtosupplier(productid,supplierid).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)

    contract,web3=connect_with_register(0)
    _dids,_dnames,_dcontacts,_daddress,_demails,_dphones,_dtins,_dbrns,_dwallets,_demergency,_dpasswords=contract.functions.viewDistributors().call()
    _sids,_snames,_scontacts,_saddress,_semails,_sphones,_stins,_sbrns,_swallets,_semergency,_spasswords=contract.functions.viewSuppliers().call()
    _tdistributor,_tproduct=contract.functions.viewDistribution().call()
    _productId,_productName,_manufacturerInfo,_lotNumber,_manufacturingDate,_expirationDate,_serialNumber,_uid,_productstatus=contract.functions.viewProducts().call()
    data1=[]
    for i in range(len(_tdistributor)):
        print(_dids,_tdistributor)
        dindex=_dids.index(int(_tdistributor[i]))
        dwallet=_dwallets[dindex]
        print(dwallet)
        if dwallet==session['username']:
            pindex=_productId.index(_tproduct[i])
            if _productstatus[pindex]==1:
                dummy=[]
                dummy.append(_productId[pindex])
                dummy.append(_productName[pindex])
                data1.append(dummy)
                print(data1)

    data2=[]
    _sids,_snames,_scontacts,_saddress,_semails,_sphones,_stins,_sbrns,_swallets,_semergency,_spasswords=contract.functions.viewSuppliers().call()
    for i in range(len(_sids)):
        dummy=[]
        dummy.append(_sids[i])
        dummy.append(_snames[i])
        data2.append(dummy)

    
    return render_template('sendtosupplier.html',l1=len(data1),l2=len(data2),dashboard_data1=data1,dashboard_data2=data2)

@app.route('/sendtodistributorform',methods=['post'])
def sendtodistributorform():
    productid=request.form['productid']
    distributorid=request.form['distributorid']
    print(productid,distributorid)
    contract,web3=connect_with_register(0)
    tx_hash=contract.functions.sendtodistributor(productid,distributorid).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)

    contract,web3=connect_with_register(0)
    _dids,_dnames,_dcontacts,_daddress,_demails,_dphones,_dtins,_dbrns,_dwallets,_demergency,_dpasswords=contract.functions.viewDistributors().call()
    data1=[]
    for i in range(len(_dids)):
        dummy=[]
        dummy.append(_dids[i])
        dummy.append(_dnames[i])    
        data1.append(dummy)
    data2=[]
    _productId,_productName,_manufacturerInfo,_lotNumber,_manufacturingDate,_expirationDate,_serialNumber,_uid,_productstatus=contract.functions.viewProducts().call()
    for i in range(len(_productId)):
        if _productstatus[i]==0:
            dummy=[]
            dummy.append(_productId[i])
            dummy.append(_productName[i])
            data2.append(dummy)
    print(data1,data2,'hi')
    return render_template('sendtodistributor.html',l1=len(data2),l2=len(data1),dashboard_data1=data2,dashboard_data2=data1)

@app.route('/searchproduct',methods=['post','get'])
def searchproduct():
    if request.method=='POST':
        productid=request.form['productid']
    else:
        productid=request.args.get('productid')
    print('hi', productid)
    contract,web3=connect_with_register(0)
    _ssupplier,_sproduct=contract.functions.viewSupply().call()
    if str(productid) in _sproduct:
        data=[]
        data.append(productid)
        _productId,_productName,_manufacturerInfo,_lotNumber,_manufacturingDate,_expirationDate,_serialNumber,_uid,_productstatus=contract.functions.viewProducts().call()
        pindex=_productId.index(str(productid))
        data.append(_productName[pindex])
        data.append(_manufacturerInfo[pindex])
        _tdistributor,_tproduct=contract.functions.viewDistribution().call()
        dindex=_tproduct.index(str(productid))
        distributor=_tdistributor[dindex]
        _dids,_dnames,_dcontacts,_daddress,_demails,_dphones,_dtins,_dbrns,_dwallets,_demergency,_dpasswords=contract.functions.viewDistributors().call()
        dindex2=_dids.index(int(distributor))
        data.append(_dnames[dindex2])
        sindex=_sproduct.index(str(productid))
        supplier=_ssupplier[sindex]
        _sids,_snames,_scontacts,_saddress,_semails,_sphones,_stins,_sbrns,_swallets,_semergency,_spasswords=contract.functions.viewSuppliers().call()
        sindex2=_sids.index(int(supplier))
        data.append(_snames[sindex2])
        data.append(_manufacturingDate[pindex])
        data.append(_expirationDate[pindex])


        return render_template('index.html',data=data)
    else:
        return render_template('index.html',data=['NA','NA','NA','NA','NA','NA','NA'])
    return redirect('/')

if __name__=="__main__":
    app.run('0.0.0.0',port=5001,debug=True)