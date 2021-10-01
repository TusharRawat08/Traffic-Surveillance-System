def process_ocr(labels, image):
    #print(image.shape[0]/image.shape[1])
    if (image.shape[0]/image.shape[1]>0.4):
        upper = []
        lower = []
        y_thresh = image.shape[0]
    
        for i in labels:
            #print(i[0][1])
            #print(y_thresh//3.2)
            if i[0][1]>y_thresh//3.2:
                lower.append(i)
            else:
                upper.append(i)
        
        upper = sorting_alongx(upper)
        lower = sorting_alongx(lower)
        final = upper + lower
        #print(final)
    else:
        final = sorting_alongx(labels)
    
    label = ""
    for i in final:
        label+=i[1][0]

    return label

def sorting_alongx(l):
    for i in range(len(l)):
        for j in range(i+1,len(l)):
            #print(l[j][0][0], l[i][0][0])
            if l[i][0][0]>l[j][0][0]:
                l[i],l[j]=l[j],l[i]
    return l
