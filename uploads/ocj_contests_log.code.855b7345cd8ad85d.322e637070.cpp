#include <stdio.h>
#include <iostream>
#include <string.h>

using namespace std;

int main()
{
	int t, len, last1cal = 0, last2cal = 0, last3cal = 0, sum;
	cin>>t;
	while(t--)
	{
		cin>>len;
		int input[len], dp[len][3];
		for (int i = 0; i < len; ++i)
			for (int j = i,input[i] = 0; j < 3; ++j)
				dp[i][j] = 0;

		for (int i = 0; i < len; ++i)
			cin>>input[i];

		dp[0][0] = input[0];
		dp[0][1] = input[1];
		dp[0][2] = input[2];

		for(int i = 0; i < len; ++i)
		{
			if(last1cal != 1)
			
{				for (int j = i,sum = 0; j <= i  && j <len; ++j)
				{
					dp[i][j] = sum + input[j];
					sum = dp[i][j];
				}
				last1cal = 1;
			}
			else
				last1cal = 0;

			if(last2cal != 2)
			{
				for (int j = i; j <= i+2  && j <len; ++j)
				{
					dp[i][j] = sum + input[j];
					sum = dp[i][j];
				}
				last1cal = 0;
			}
			else
				last2cal++;

			if(last3cal != 3)
			{
				for (int j = i; j <= i+3  && j <len; ++j)
				{
					dp[i][j] = sum + input[j];
					sum = dp[i][j];
				}
				last3cal = 0;
			}
			else
				last3cal++;


		}

		for(int i = 0; i < len; ++i)
		{
			for (int j = i ; j < i + 3 && j <len; ++j)
			{
				cout<<dp[i][j]<<" ";
			}
			cout<<endl;
		}
	}

	return 0;
}