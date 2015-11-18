/*

As we all now , Barney has an awesome "PLAYBOOK" , which is very huge in size and has lots of pages. Now Ted has borrowed his playbook for few days , After careful reading he finds out the most successful plays executed by Barney are given on the pages having the prime numbers. Since Ted envies Barney he tears out all the prime number pages from the playbook and returns the playbook to Barney.

Now on the friday evening , Barney opens the playbook on the page p1 and scrolls continuosly till the page p2 , He figures out that certain pages are missing , As we all know, that Barney is weak in Mathematics , You have to tell him what all page numbers are missing.
Input
-----------
First line has the number of test cases t , ( t < = 10 ). In each line has the page numbers p1 and p2 separated by space.
Constraints : 1 <= p1 <= p2 <= 10^10
p2-p1 <= 10^5
Output
-----------
For each test case print all missing page numbers p such that p1 <= p <= p2, one number per line.
Test cases are separated by and empty line.
Example
Input:
2
4 6
5 7

Output:
5

5
7

*/



#include <iostream>

using namespace std;

int main()
{
	long long int t,a,b,i,j,sieve[100000],prime[100000],MAX,p_count=0,p_range[100000],current_prime,segment;
	MAX = 100000;
	sieve[1]=0;

	//Intilize bot the array with 1
	for(i=2;i<=MAX;i++)
		sieve[i]=1;
		
	//Calculate the Prime numbers
	for(i=2; i*i<=MAX; i++)
        if(sieve[i])
            for(j=2*i ; j<=MAX; j+=i)
    			sieve[j]=0;

   	//Store the seive numbers
   	for(i=2;i<=MAX; i++)
    	if(sieve[i])
    		prime[p_count++]=i;

	cin>>t;
	while(t--)
	{
		cin>>a>>b;
		if(a < 2) a = 2;
	    for(i=0;i<=(b-a); i++)
    		p_range[i]=1;
	    for(i=0; ;i++)
	    {
	    	current_prime = prime[i];

	    	if(current_prime*current_prime > b)
    			break;
    		segment = (a/current_prime)*current_prime;
    		
    		if(segment<a)
    			segment+=current_prime;
    		if(segment==current_prime)
    			segment+=current_prime;

	        for(; segment<=b; segment+=current_prime)
	        	p_range[segment-a]=0;
	    }

		//Display the seive numbers
		for (i=0;i<=(b-a);i++)
		{
			if(p_range[i])
				cout<<i+a<<endl;
		}
		cout<<endl;
	}
	return 0;
}