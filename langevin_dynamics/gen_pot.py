# to geneate potential energy file
# a double well potential is used here
# y=(b-c*x**2)**2

output = open('potential.txt','w')
output.write('# index postion potential force\n')
for i in range(1,8002):
    x = 0.001*(i - 4001)
    y = x**4-2*x**2+1
    f = 4*x**3-4*x+1
#    f.write(i,x,y,f)
#    output.write(i,x,y,f)
    print('{:4d} {:7.3f} {:10.7f} {:11.7f}'.format(i,x,y,f),file=output)
#    print('{}'.format(i),'{}'.format(x),'{}'.format(y),'{}'.format(f),file=output)
#f.close()
