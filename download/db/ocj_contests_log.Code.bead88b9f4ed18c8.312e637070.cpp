#include <iostream>
#include <vector>

using namespace std;

int main()
{
	unsigned long long int t, n, temp, flag, m, i, j;
	cin>>t;
	while(t--)
	{
		flag = 0;
		cin>>n>>m;

		if(n > m)
		{
			for(i = 0; i < n; i++)
				cin>>temp;
			cout<<"YES"<<endl;
			continue;
		}
		else
		{
			if(n == 1)
			{
				cin>>temp;
				if(temp%m == 0)
					cout<<"YES"<<endl;
				else
					cout<<"NO"<<endl;
				continue;
			}

			vector <vector <unsigned long long int> > sumset(10*m + 10, vector<unsigned long long int>(n+10,0));
			vector <unsigned long long int> input(n+10,0);

			for(i = 0; i < n; i++)
			{
				cin>>temp;
				if(flag == 1)
					continue;
				else
				{
					if((input[i] = temp%m) == 0)
						flag = 1;
				}
			}
			if(flag == 1)
			{
				cout<<"YES"<<endl;
				continue;
			}
			flag=0;
			for (i = 0; i <= n; i++)
      			sumset[0][i] = true;
      	    for (i = 1; i <= 10*m + 5; i++)
     		{
       			for (j = 1; j <= n; j++)
       			{
         			sumset[i][j] = sumset[i][j-1];
         			if (i >= input[j-1])
         			{
           				sumset[i][j] = sumset[i][j] || sumset[i - input[j-1]][j-1];
           				if(i%m == 0 && sumset[i][j] == 1)
           				{
           					flag = 1;
           					break;
           				}
           			}
           		}
           		if(flag == 1)
           			break;
           	}
           	if(flag)
           		cout<<"YES"<<endl;
           	else
           		cout<<"NO"<<endl;
       }
    }
    return 0;
}