#include <iostream>
#include <string.h>

using namespace std;

long long int t, input[100001], len,dp[100001], i;

long long int sumEaring(long long int a)
{
	if(a>=len)
		return 0;

	if(dp[a] != -1)
		return dp[a];	

	if(a+2<len)
		return dp[a] = max(input[a] + sumEaring(a+2),max(input[a]+input[a+1] + sumEaring(a+4), input[a]+input[a+1]+input[a+2]+sumEaring(a+6)));
	else if(a+1 < len)
		return dp[a] = max(input[a] + sumEaring(a+2),input[a]+input[a+1] + sumEaring(a+4));
	return 0;
}


int main()
{
	cin>>t;
	while(t--)
	{
		cin>>len;
		memset(dp, -1, sizeof dp);
		
		for(i = 0; i<len;i++)
			cin>>input[i];
		if(len >= 3)
			cout<<max(input[0] + sumEaring(2),max(input[0]+input[1]+sumEaring(4), input[0]+input[1]+input[2]+sumEaring(6)))<<endl;
		else if(len == 2)
			cout<<max(input[0] + sumEaring(2),input[0]+input[1]+sumEaring(4))<<endl;
		else
			cout<<input[0] + sumEaring(2)<<endl;
	}
	return 0;
}