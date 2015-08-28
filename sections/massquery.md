Outlined here is a general pattern for doing a mass query using OData. 

#### Simple approach

Outlined below is the simple approach to do an OData query using the standard system query options.

```
GET /CustomerCollection?$inlinecount=allpages&$format=json&$filter=$ID eq '12345' or $ID eq '567879'...
```

In some situations, where larger number of $filter conditions, this approach might not work due to URL length restrictions. In these situations the best approach is to use the $batch to do a mass GET.

#### $batch approach
