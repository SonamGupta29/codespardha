#include <iostream>

using namespace std;

int main()
{
	unsigned long long int t, no, prod, ans;
	cin>>t;
	while(t--)
	{
		cin>>no;
		prod = 5;
		ans = 0;
		while(prod <= no)
		{
			ans += no/prod;
			prod=prod*5;
		}
		cout<<ans;
		if(t != 1)
			cout<<endl;
	}
	
}
