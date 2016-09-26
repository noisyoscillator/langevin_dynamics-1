# to geneate potential energy file
# a double well potential is used here
# y=c(b-a*x**2)**2

output = open('potential.txt','w')
output.write('# index postion potential force\n')

# parameters for potential energy function
a = 1
b = 1
c = 1
# range
n = 8001 # intended upper limit +1

for i in range(-n,n):
    x = 0.001*i
    y = c*(b-a*x**2)**2
    f = 4*a*c*x*(b-a*x**2)
#    f.write(i,x,y,f)
#    output.write(i,x,y,f)
    print('{:4d} {:7.3f} {:10.7f} {:11.7f}'.format(i+n+1,x,y,f),file=output)
#    print('{}'.format(i),'{}'.format(x),'{}'.format(y),'{}'.format(f),file=output)
#f.close()
