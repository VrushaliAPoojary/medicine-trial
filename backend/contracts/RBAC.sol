// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RBAC {
    enum Role { None, Admin, Company, Doctor, Auditor, Patient }

    struct UserInfo {
        string name;
        string physicalAddress;
        address walletAddress; // ✅ Store the wallet address
        Role role;
        bool isRegistered;
    }

    struct RoleRequest {
        Role requestedRole;
        bool isPending;
    }

    mapping(address => UserInfo) public users;
    mapping(address => RoleRequest) public roleRequests;

    address public immutable deployer;

    event UserRegistered(address indexed user, string name, string physicalAddress, address walletAddress);
    event RoleRequested(address indexed user, Role role);
    event RoleAssigned(address indexed user, Role role);

    modifier onlyRole(Role _role) {
        require(users[msg.sender].role == _role, "Unauthorized: Incorrect Role");
        _;
    }

    modifier onlyDeployer() {
        require(msg.sender == deployer, "Unauthorized: Only Deployer");
        _;
    }

    constructor() {
        deployer = msg.sender;
        users[msg.sender] = UserInfo({
            name: "Admin",
            physicalAddress: "Admin Location",
            walletAddress: msg.sender,
            role: Role.Admin,
            isRegistered: true
        });
        emit RoleAssigned(msg.sender, Role.Admin);
    }

    function registerUser(string calldata _name, string calldata _physicalAddress) external {
        require(!users[msg.sender].isRegistered, "User already registered");

        users[msg.sender] = UserInfo({
            name: _name,
            physicalAddress: _physicalAddress,
            walletAddress: msg.sender,  // ✅ Store msg.sender as wallet address
            role: Role.None,
            isRegistered: true
        });

        emit UserRegistered(msg.sender, _name, _physicalAddress, msg.sender);
    }

    function requestRole(Role _role) external {
        require(users[msg.sender].isRegistered, "User must be registered first");
        require(_role != Role.None && _role != Role.Admin, "Invalid role request");
        require(!roleRequests[msg.sender].isPending, "Already requested");
        require(users[msg.sender].role == Role.None, "Role already assigned");

        roleRequests[msg.sender] = RoleRequest({requestedRole: _role, isPending: true});
        emit RoleRequested(msg.sender, _role);
    }

    function approveRole(address _user) external onlyRole(Role.Admin) onlyDeployer {
        require(roleRequests[_user].isPending, "No pending request");

        Role assignedRole = roleRequests[_user].requestedRole;
        users[_user].role = assignedRole;
        roleRequests[_user].isPending = false;

        emit RoleAssigned(_user, assignedRole);
    }

    function getRole(address _user) external view returns (Role) {
        return users[_user].role;
    }

    function getUser(address _user)  external view returns (  
    string memory name,
    string memory physicalAddress,
    address walletAddress,
    Role role,
    bool isRegistered)
    {
    require(users[_user].isRegistered, "User not found");
    
    UserInfo memory user = users[_user];
    return (user.name, user.physicalAddress, user.walletAddress, user.role, user.isRegistered);
    }
}
