
SELECT public.ed2011b.ed2011_ed11form,
public.ed2011b.ed2011_ed11form,
public.ed2011b.ed2011_ed11form,
--- 3 identical columns for space keeping
public.ed2011b.l0101104, 
public.ed2011b.l020100, public.ed2011b.l020105,
public.ed2011b.l020106, public.ed2011b.l020107,
public.ed2011b.l060100, 
public.ed2011b.l060101,public.ed2011b.l060105, 
public.ed2011b.l060106, public.ed2011b.l060107, 
public.ed2011b.l060111, public.ed2011b.l060800, 
public.ed2011b.l060802
FROM public.ed2011b 
Join public.ed2016b
on   public.ed2011b.ed2011_ed11form=public.ed2016b.ed2016_ed11form
order by public.ed2011b.ed2011_ed11form asc
LIMIT 10000

