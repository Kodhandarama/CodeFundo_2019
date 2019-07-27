[![Board Status](https://dev.azure.com/Stallions-A/ace3487f-cac5-47f2-b8fb-2b2907197500/d90cab1c-eb8d-4fbd-b0ac-7ad84547dcea/_apis/work/boardbadge/52174574-a8f7-4b9f-9cf1-01b5288acbcc?columnOptions=1)](https://dev.azure.com/Stallions-A/ace3487f-cac5-47f2-b8fb-2b2907197500/_boards/board/t/d90cab1c-eb8d-4fbd-b0ac-7ad84547dcea/Microsoft.RequirementCategory/)
[![Build Status](https://dev.azure.com/Stallions-A/Codefundo/_apis/build/status/Darth-Kronos.CodeFundo_2019?branchName=master)](https://dev.azure.com/Stallions-A/Codefundo/_build/latest?definitionId=3&branchName=master)
# CodeFundo_2019
# Idea for codefundo++

We intend to build a safe, secure and fast end to end solution for the elections in India.

The current election process is tedious, messy and inefficient.

Right off the bat, the creation of electoral rolls is a labor-intensive process.
Before every election, there is a manual census that is conducted from door to door.

There has to be a better way!

We intend to create our own self- sufficient database for this process.

This is created in the first election and is updated in every election following that. We plan to hold the registration process right before the election, in the polling booth itself. It is a fairly quick process in which an individual can procure his voter ID.

All we need is an ID(to make sure that the person is who he says he is), address proof(to ensure that he is voting in the right constituency) and Aadhar ID(for unique identification).

We are also going to automate the candidate registration in which people of the society plan to stand for the elections. This is a long drawn process in the current scheme of things. We plan to make this fair, easy and transparent.

In this part, all the candidate has to do is authenticate his approval by providing his ID and then provide basic information which pertains to the constituency for which he/she wishes to announce his/ her candidature.

Now, coming to the actual voting process.

We plan to install a node in each polling booth. There is a manual authentication done in each poll to check the eligibility of the voter. Once eligibility is confirmed, the officer enters the voter’s voter ID into his system. The voter then votes for his choice of the party by clicking on the appropriate symbol.

Every time a vote is cast a new block is created which eventually forms a block-chain. Each constituency will have its own chain to ease the process of calculating the result. Eventually, all these chains can be parsed to obtain the final result.

This process makes sure that the voting process is secure. As any changes made to any casted vote (block) will disrupt the entire chain and hence cannot be done.

We intend to use the Azure web App service to deploy our website. Azure pipeline is a cloud service that we can use to automatically build and test our code. Therefore any commits in our Github repository, Azure pipeline automatically deploys the commits to our website. Azure Blockchain Workbench is a collection of Azure services designed to help us create and deploy blockchain applications.

Therefore, by using Azure blockchain and its web service, we plan to build a Proof-of-Concept to demonstrate how the voting process can be made more secure, transparent and reliable by simulating the real-world data with our databases.
