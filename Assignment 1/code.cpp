#include<iostream>
#include<string>
#include<cmath>
using namespace std;

string hex_to_bin(int inp)
{
  string op = "";
  int a[4],i=0;
  for(int j=0;j<4;j++)
     a[j]=0;
  if(inp>=97)
     inp = inp-87;
  else if(inp>=65)
     inp = inp-55;
  else
     inp = inp-48;
  int num=inp;
  while(num>0&&i<4)
  {
   a[i++]=(num%2);
   num = num/2;
  }
  for(int i=3;i>=0;i--)
      op = op + to_string(a[i]);
  return op;
}

string bin_to_hex(string inp)
{
  string temp="";
  int size = inp.length()/4;
  for(int j=0;j<size;j++)
  {
  int t=0;
  for(int i=0;i<4;i++)
  {
    t = t + (int(inp[3-i+(4*j)])-48)*pow(2,i);
  }
  if(t>9)
     temp=temp+char(t+55);
  else
     temp = temp+to_string(t);
  }
  return temp;
     
}

void init_per(int p[])
{
  int a[]={58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
           57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7};
  int d[64];
  for(int i=0;i<64;i++)
      d[i]=p[a[i]-1];
  for(int i=0;i<64;i++)
      p[i]=d[i];
}

void xxor(int p[],int k[],int n)
{
  for(int i=0;i<n;i++)
  {
    if(p[i]==k[i])
       p[i]=0;
    else
       p[i]=1;
  }
}

void s_box(int in[],int out[])
{
    int s1[4][16]=
    {
        14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
        0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
        4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
        15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13
    };

    int s2[4][16]=
    {
        15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
        3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
        0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
        13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9
    };

    int s3[4][16]=
    {
        10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
        13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
        13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
        1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12
    };

    int s4[4][16]=
    {
        7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
        13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
        10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
        3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14
    };

    int s5[4][16]=
    {
        2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
        14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
        4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
        11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3
    };

    int s6[4][16]=
    {
        12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
        10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
        9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
        4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13
    };

    int s7[4][16]=
    {
        4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
        13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
        1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
        6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12
    };

    int s8[4][16]=
    {
        13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
        1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
        7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
        2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11
    };
    string dmy="";
    int i=0,m=0;
    for(int i=0;i<8;i++)
    {
      int t1,t2,val;
      string temp="";
      string temp2="00";
      for(int j=0;j<4;j++)
	 temp = temp+to_string(in[m+j+1]);
      temp2=temp2+to_string(in[m]);
      temp2=temp2+to_string(in[m+5]);
      m=m+6;
      temp=bin_to_hex(temp);
      temp2=bin_to_hex(temp2);
      if(int(temp[0])>=65)
      	t1=int(temp[0])-55;
      else
        t1=int(temp[0])-48;
      t2=int(temp2[0])-48;
      switch(i)
      {
        case 0:
	   val=s1[t2][t1];
	   break;
	case 1:
	   val=s2[t2][t1];
	   break;
	case 2:
	   val=s3[t2][t1];
	   break;
	case 3:
	   val=s4[t2][t1];
	   break;
	case 4:
	   val=s5[t2][t1];
	   break;
	case 5:
	   val=s6[t2][t1];
	   break;
	case 6:
	   val=s7[t2][t1];
	   break;
	case 7:
	   val=s8[t2][t1];
	   break;
	default:
	   val=0;
      } 
      if(val>9)
	dmy= dmy+hex_to_bin(val+55);
      else
	dmy=dmy+hex_to_bin(val+48);
    }
    for(string::iterator it=dmy.begin();it!=dmy.end();it++)
        out[i++]=int(*it)-48;
}

void str_box(int in[])
{
  int a[]={16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25};
  int dmy[32];
  for(int i=0;i<32;i++)
     dmy[i]=in[a[i]-1];
  for(int i=0;i<32;i++)
     in[i]=dmy[i];
}

void f_box(int p[],int k[])
{
 int a[]={32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,
	  28,29,30,31,32,1};
 int dmy[48],s_out[32];
 for(int i=0;i<48;i++)
    dmy[i]=p[a[i]-1];
 xxor(dmy,k,48);
 s_box(dmy,s_out);
 str_box(s_out);
 for(int i=0;i<32;i++)
    p[i]=s_out[i];
}

void final_per(int p[])
{
  int a[]={40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,
	   36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25};
  int dmy[64];
  for(int i=0;i<64;i++)
     dmy[i]=p[a[i]-1];
  for(int i=0;i<64;i++)
     p[i]=dmy[i];
}

void encryption(int p[],string keys[])
{
  string dmy="";
  for(int i=0;i<64;i++)
      dmy = dmy + to_string(p[i]); 
  cout<<"\nENCRYPTION:\nInput Plaintext : "<<bin_to_hex(dmy)<<"\n";
  dmy = "";
  init_per(p);  
  int k[48],l[32],r[32],s[32];
  for(int i=0;i<64;i++)
      dmy = dmy + to_string(p[i]); 
  
  cout<<"After initial permutation : "<<bin_to_hex(dmy)<<"\n";
  for(int i=0;i<16;i++)
  {
    string t="";
    int m=0;
    for(string::iterator it=keys[i].begin();it!=keys[i].end();it++)
        k[m++]=int(*it)-48; 
    for(int j=0;j<32;j++)
       l[j]=p[j];
    for(int j=0;j<32;j++)
    { r[j]=p[j+32];s[j]=p[j+32];}
   f_box(r,k);
   xxor(l,r,32); 
   for(int j=0;j<32;j++)
      p[j]=s[j];
   for(int j=0;j<32;j++)
      p[j+32]=l[j];
   if(i==15)
   {
     for(int j=0;j<32;j++)
      p[j]=l[j];
     for(int j=0;j<32;j++)
      p[j+32]=s[j];
   }
   for(int j=0;j<64;j++)
      t=t+to_string(p[j]);
   cout<<"After round "<<i+1<<" : "<<bin_to_hex(t)<<"\n";
  }
  final_per(p);
  string tem="";
  for(int j=0;j<64;j++)
      tem=tem+to_string(p[j]);
  cout<<"After final permutation : "<<bin_to_hex(tem)<<"\n";
  cout<<"Final ciphertext : "<<bin_to_hex(tem)<<"\n";

}

void par_drop(int k[],int out[])
{ 
 int a[]={57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,
	  31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4};
 for(int i=0;i<56;i++)
    out[i]=k[a[i]-1]; 

}

void shift_left(int in[])
{
 int a[28];
 for(int i=0;i<27;i++)
    a[i]=in[i+1];
 a[27]=in[0];
 for(int i=0;i<28;i++)
    in[i]=a[i];
}

string comp_box(string key)
{
  string temp = "";
  temp.resize(48);
  int a[48] = {14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,
	       48,44,49,39,56,34,53,46,42,50,36,29,32};
  for(int i=0;i<48;i++)
     temp[i] = key[a[i]-1];

  return temp;
}

void key_gen(int k[],string keys[])
{
  cout<<"\nKEYS : \n";
  int dmy[56],l[28],r[28];
  string temp="";
  par_drop(k,dmy);  
  cout<<"After parity drop : ";
  for(int i=0;i<56;i++)
     temp=temp+to_string(dmy[i]);
  cout<<bin_to_hex(temp)<<"\n";
  for(int j=0;j<28;j++)
  {
      l[j]=dmy[j]; 
      r[j]=dmy[j+28];
  }
  for(int i=0;i<16;i++)
  {
    keys[i]="";
    temp="";
    if((i!=0)&&(i!=1)&&(i!=8)&&(i!=15))
    {
      shift_left(l);
      shift_left(r);
    }
    shift_left(l);
    shift_left(r);
    for(int j=0;j<28;j++)
        temp=temp+to_string(l[j]);
    for(int j=0;j<28;j++)
	temp=temp+to_string(r[j]);
    keys[i]=keys[i]+comp_box(temp);
    cout<<"Round "<<i+1<<" key : "<<bin_to_hex(keys[i])<<"\n";
  }
}

void decryption(int c[],string keys[])
{
  cout<<"\nDECRYPTION :\n";
  int l[32],r[32],k[48],s[32];
  cout<<"Input ciphertext : ";
  string temp="";
  for(int i=0;i<64;i++)
     temp=temp+to_string(c[i]);
  cout<<bin_to_hex(temp)<<"\n";
  temp="";
  init_per(c);
  cout<<"After initial permutation : ";
  for(int i=0;i<64;i++)
     temp=temp+to_string(c[i]);
  cout<<bin_to_hex(temp)<<"\n";
  for(int i=0;i<16;i++)
  {
    string t="";
    string t1="";
    int m=0;
    for(string::iterator it=keys[15-i].begin();it!=keys[15-i].end();it++)
        k[m++]=int(*it)-48; 
    for(int j=0;j<32;j++)
    {
      l[j]=c[j]; r[j]=c[j+32];
      s[j]=c[j+32];
    }
    f_box(r,k);
    xxor(l,r,32);
    for(int j=0;j<32;j++)
    {
      c[j]=s[j]; c[j+32]=l[j];
    }
    for(int j=0;j<32;j++)
       t = t+to_string(l[j]);
    for(int j=0;j<32;j++)
       t1 = t1+to_string(s[j]);
    temp=""; temp=t+t1;
    cout<<"After round "<<16-i<<" "<<bin_to_hex(temp)<<"\n";
  } 
  int m=0;
  for(string::iterator it=temp.begin();it!=temp.end();it++)
     c[m++]=int(*it)-48; 
  final_per(c);
  temp="";
  cout<<"After final permutation : ";
  for(int i=0;i<64;i++)
     temp=temp+to_string(c[i]);
  cout<<bin_to_hex(temp)<<"\n";
  cout<<"Final plaintext : "; 
  cout<<bin_to_hex(temp)<<"\n";
  
}

int main()
{
  int k[64],p[64];
  int i=0;
  string keys[16];
  string plaintext,key;
  cout<<"Enter plaintext \n";
  cin>>plaintext;
  cout<<"Enter key\n";
  cin>>key;
  string p_bin="";
  string k_bin=""; 
  for(string::iterator it=plaintext.begin();it!=plaintext.end();it++)
  	p_bin = p_bin+hex_to_bin(int(*it));
  for(string::iterator it=key.begin();it!=key.end();it++)
  	k_bin = k_bin+hex_to_bin(int(*it));
  for(string::iterator it=p_bin.begin();it!=p_bin.end();it++)
     p[i++] = int(*it)-48;
  i = 0;
  for(string::iterator it=k_bin.begin();it!=k_bin.end();it++)
     k[i++] = int(*it)-48;

  key_gen(k,keys);
  encryption(p,keys);
  decryption(p,keys);
  return 0;
}
