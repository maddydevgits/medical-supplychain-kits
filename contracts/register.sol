// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {
  uint[] _dids;
  string[] _dnames;
  string[] _dcontacts;
  string[] _daddress;
  string[] _demails;
  string[] _dphones;
  string[] _dtins;
  string[] _dbrns;
  address[] _dwallets;
  string[] _demergency;
  string[] _dpasswords;

  uint[] _sids;
  string[] _snames;
  string[] _scontacts;
  string[] _saddress;
  string[] _semails;
  string[] _sphones;
  string[] _stins;
  string[] _sbrns;
  address[] _swallets;
  string[] _semergency;
  string[] _spasswords;

  string[] _productId;
  string[] _productName;
  string[] _manufacturerInfo;
  string[] _lotNumber;
  string[] _manufacturingDate;
  string[] _expirationDate;
  string[] _serialNumber;
  string[] _uid;
  uint[] _productstatus;

  string[] _tdistributor;
  string[] _tproduct;

  string[] _ssupplier;
  string[] _sproduct;


  address manufacturer;
  string manuPassword="1234";

  mapping(address=>bool) _registeredDistributors;
  mapping(address=>bool) _registeredSuppliers;
  mapping(string=>bool) _registeredProducts;
  
  constructor() {
    manufacturer=msg.sender;
  }

  modifier onlyManufacturer(){
    require(msg.sender==manufacturer);
    _;
  }

  function viewManufacturer() public view returns(address,string memory){
    return (manufacturer,manuPassword);
  }

  function addDistributor(uint did,string memory dname,string memory dcontact,string memory daddress,string memory demail,string memory dphone,string memory dtin,string memory dbrn,address wallet,string memory demergency,string memory dpassword) public onlyManufacturer{
    require(!_registeredDistributors[wallet]);

    _dids.push(did);
    _dnames.push(dname);
    _dcontacts.push(dcontact);
    _daddress.push(daddress);
    _demails.push(demail);
    _dphones.push(dphone);
    _dtins.push(dtin);
    _dbrns.push(dbrn);
    _dwallets.push(wallet);
    _demergency.push(demergency);
    _dpasswords.push(dpassword);

    _registeredDistributors[wallet]=true;
  }

  function viewDistributors() public view returns(uint[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,address[] memory,string[] memory,string[] memory) {
    return(_dids,_dnames,_dcontacts,_daddress,_demails,_dphones,_dtins,_dbrns,_dwallets,_demergency,_dpasswords);
  }

  function addSupplier(uint sid,string memory sname,string memory scontact,string memory saddress,string memory semail,string memory sphone,string memory stin,string memory sbrn,address swallet,string memory semergency,string memory spassword) public {
    require(!_registeredSuppliers[swallet]);

    _sids.push(sid);
    _snames.push(sname);
    _scontacts.push(scontact);
    _saddress.push(saddress);
    _semails.push(semail);
    _sphones.push(sphone);
    _stins.push(stin);
    _sbrns.push(sbrn);
    _swallets.push(swallet);
    _semergency.push(semergency);
    _spasswords.push(spassword);

    _registeredSuppliers[swallet]=true;
  }

  function viewSuppliers() public view returns(uint[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,address[] memory,string[] memory,string[] memory) {
    return(_sids,_snames,_scontacts,_saddress,_semails,_sphones,_stins,_sbrns,_swallets,_semergency,_spasswords);
  }

  function addProduct(
      string memory productid,
      string memory productname,
      string memory manufacturerinfo,
      string memory lotnumber,
      string memory manufacturingdate,
      string memory expirationdate,
      string memory serialnumber,
      string memory uid) public 
  {
        
        require(!_registeredProducts[productid]);
        
        _productId.push(productid);
        _productName.push(productname);
        _manufacturerInfo.push(manufacturerinfo);
        _lotNumber.push(lotnumber);
        _manufacturingDate.push(manufacturingdate);
        _expirationDate.push(expirationdate);
        _serialNumber.push(serialnumber);
        _uid.push(uid);
        _productstatus.push(0);

        _registeredProducts[productid]=true;
  }

  function viewProducts() public view returns(string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory,uint[] memory){
    return (
      _productId,
      _productName,
      _manufacturerInfo,
      _lotNumber,
      _manufacturingDate,
      _expirationDate,
      _serialNumber,
      _uid,
      _productstatus);
  }

  function sendtodistributor(string memory productid,string memory distributorid) public {

    uint i;
    for(i=0;i<_productId.length;i++){
      if((keccak256(abi.encodePacked(productid)) == keccak256(abi.encodePacked(_productId[i])))){
        require(_productstatus[i]==0);
        _productstatus[i]=1;
        _tdistributor.push(distributorid);
        _tproduct.push(productid);
      }
    }
  }

  function viewDistribution() public view returns(string[] memory,string[] memory){
    return(_tdistributor,_tproduct);
  }

  function sendtosupplier(string memory productid,string memory supplierid) public {
    uint i;
    for(i=0;i<_productId.length;i++){
      if((keccak256(abi.encodePacked(productid)) == keccak256(abi.encodePacked(_productId[i])))){
        require(_productstatus[i]==1);
        _productstatus[i]=2;
        _ssupplier.push(supplierid);
        _sproduct.push(productid);
      }
    }
  }

  function viewSupply() public view returns(string[] memory,string[] memory){
    return(_ssupplier,_sproduct);
  }

}
