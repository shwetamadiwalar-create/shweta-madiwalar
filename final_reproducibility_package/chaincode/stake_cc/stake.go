package main
import "github.com/hyperledger/fabric-contract-api-go/contractapi"
type StakeContract struct{ contractapi.Contract }
func main(){ cc,_ := contractapi.NewChaincode(new(StakeContract)); cc.Start() }
