#include <bits/stdc++.h>

using namespace std;

int main()
{
	int t, input[100], dp[100], len,i ,j;

	cin>>t;

	while(t--)
	{
		memset(dp , -1 ,sizeof dp);

		cin>>len;

		for(i = 0; i < len; i++)
			cin>>input[i];

		dp[0] = input[len-1];
		dp[1] = input[len-2] + dp[0];
		dp[2] = input[len-3] + dp[1];

		for(j = len-1, i = 3; j >= 0; j--, i++)
		{
			dp[i] = input[j] + max(dp[i-2],max(dp[i-3],dp[i-4]));
		}

		for (int i = 0; i < len; ++i)
		{
			cout<<dp[i]<<" ";
		}
		
	}
	return 0;
}