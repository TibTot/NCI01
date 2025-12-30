SELECT public.ed2022b.ed2022_ed11form,
public.ed2022b.ed2022_ed11form,
public.ed2022b.ed2022_ed11form,
/*public."ED2011Core01".county,public."ED2011Core01".countyname,*/
public.ed2022b.w0101104, 
public.ed2022b.w020100, public.ed2022b.w020105,
public.ed2022b.w020106, 
public.ed2022b.w020103,
public.ed2022b.w060100, 
public.ed2022b.w060101,public.ed2022b.w060104, 
public.ed2022b.w060105, public.ed2022b.w060106, 
public.ed2022b.w060109, public.ed2022b.w060800, 
public.ed2022b.w060804
FROM public.ed2022b 
Join public.ed2011b
on   public.ed2022b.ed2022_ed11form=public.ed2011b.ed2011_ed11form
order by public.ed2011b.ed2011_ed11form asc
LIMIT 10000


