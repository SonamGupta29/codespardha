/*

------ Ted's best friend ------

Barney Stinson and Marshall are playing a game to decide who is Ted's best friend . The one who
wins will finally be the best man on the Ted's Wedding . To play this game, lily has given them lot of playing cards, these cards are different from the ordinary playing cards . On each card a positive number is written.
Now, to play this game Lily randomly picks 'n' cards and lays them down on the ground in a huge pile.
She asks them to find all the prime divisors of the LCM of these n numbers.
Since Marshall and Barney are both weak in mathematics they turn to you for help!

Input
-------------------------
First line of the input contains an integer T, the number of test cases. Then T test cases follow. Each test case consists of a single integer n. Next line contains n integers(space separated), a1,a2,..,an.

Output
-------------------------
For each test case, print Case #X: M where M is the number of prime divisors of lcm(a1,a2,..,an) and then M lines with the prime divisors in non-decreasing order.

Example
-------------------------
Input:
1
8
1 2 3 4 5 6 7 8

Output:
Case #1: 4
2
3
5
7

Constraints:

T <= 100 1 <= N <= 100 1 <= ai <= 10^12

*/


#include <iostream>

using namespace std;

int main()
{
	unsigned long long int seive[1000000],i,j,no,MAX,t,len,fcnt,ctr = 0,output[1000],ti,k,primes[10000],temp,lc;

	MAX = 1000000;
	
	for(i=0;i<MAX;i++)
		seive[i] = 1;
	
	for(i=2;i<MAX;i++)
		for(j=i*i;j<MAX;j+=i)
			seive[j] = 0;

	for(i=2;i<MAX;i++)
		if(seive[i])
			primes[ctr++]=i;

	cin>>t;
	
	for(ti=1;ti<=t;ti++)
	{
		ctr = 0;
		fcnt = 0;

		cin>>len;
	
		for(i=0;i<len;i++)
		{
			cin>>no;
			if(no == 1) continue;
			for(j=0;primes[j]<=no && primes[j]<999983;j++)
			{
				if(no%primes[j] == 0)
				{
					output[ctr++] = primes[j];
					while(no%primes[j] == 0)
						no /= primes[j];						
				}
			}                                                                                                                             
			if(no>999983) output[ctr++] = no;
		}		
	    for (i = 1; i < ctr; i++)
	    {
		    for (j = i; j >= 1; j--)
			{
				if (output[j] < output[j-1])
	            {
	                temp = output[j];
    	            output[j] = output[j-1];
        	        output[j-1] = temp;
            	}
	            else
	                break;
			}
		}
		for(k=0;k<ctr;k++)
			if(lc!=output[k])
			{
				fcnt++;
				lc = output[k];
			}

		cout<<"Case #"<<ti<<": "<<fcnt<<endl;
		lc = 0;
		for(k=0;k<ctr;k++)
		{
			if(lc!=output[k])
			{
				cout<<output[k]<<endl;
				lc = output[k];
			}
		}
	}
	return 0;
}
