// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {

  string[] _distributornames;
  address[] _distributorwallets;
  string[] _distributoremails;
  string[] _distributormobiles;
  string[] _distributoraddress;
  string[] _distributorpasswords;

  string[] _suppliernames;
  address[] _supplierwallets;
  string[] _supplieremails;
  string[] _suppliermobiles;
  string[] _supplieraddress;
  string[] _supplierpasswords;

  address manufacturer;
  mapping(address=>bool) _registeredDistributors;
  
  constructor() {
    manufacturer=msg.sender;
  }

  modifier onlyManufacturer(){
    require(msg.sender==manufacturer);
    _;
  }

  function addDistributor(address distributorwallet,string memory distributorname,string memory distributoremail,string memory distributormobile,string memory distributoraddress,string memory password) public onlyManufacturer{
    require(_registeredDistributors[distributorwallet]);

    _distributorwallets.push(distributorwallet);
    _distributornames.push(distributorname);
    _distributoremails.push(distributoremail);
    _distributormobiles.push(distributormobile);
    _distributoraddress.push(distributoraddress);
    _distributorpasswords.push(password);

    _registeredDistributors[distributorwallet]=true;
  }

  function viewDistributors() public view returns(address[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory) {
    return(_distributorwallets,_distributornames,_distributoremails,_distributormobiles,_distributoraddress,_distributorpasswords);
  }

  function addSupplier(address supplierwallet,string memory suppliername,string memory supplieremail,string memory suppliermobile,string memory supplieraddress,string memory password) public onlyManufacturer{
    require(_registeredDistributors[supplierwallet]);

    _supplierwallets.push(supplierwallet);
    _suppliernames.push(suppliername);
    _supplieremails.push(supplieremail);
    _suppliermobiles.push(suppliermobile);
    _supplieraddress.push(supplieraddress);
    _supplierpasswords.push(password);

    _registeredDistributors[supplierwallet]=true;
  }

  function viewSuppliers() public view returns(address[] memory,string[] memory,string[] memory,string[] memory,string[] memory,string[] memory) {
    return(_supplierwallets,_suppliernames,_supplieremails,_suppliermobiles,_supplieraddress,_supplierpasswords);
  }

}
