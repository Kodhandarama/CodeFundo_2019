pragma solidity >=0.4.25 <0.6.0;
import "./Election.sol";

contract Voter {
    enum StateType {VoterRegistered, VoteCasted}

    StateType public State;
    address public ElectionCommission;
    int public Const_ID;
    int[] public Candidates;
    address public ParentContract;
    string public VoterID;

    constructor(int const_ID, address parentContractAddress, string memory Voter_ID, address electionCommission) public
    {
        ElectionCommission = electionCommission;
        Const_ID = int(const_ID);
        VoterID = Voter_ID;
        ParentContract = parentContractAddress;
        State = StateType.VoterRegistered;
    }

    function Voting(int Candidate_ID) public
    {
        Election election = Election(ParentContract);
        election.update(Candidate_ID);
        State = StateType.VoteCasted;
    }
}