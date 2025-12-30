SELECT public.ed2016b.ed2016_ed11form,
public.ed2016b.ed2016_ed11form,
public.ed2016b.ed2016_ed11form,
---3 identical columns space keeping,
public.ed2016b.s0101104, 
public.ed2016b.s020100, public.ed2016b.s020105,
public.ed2016b.s020106, public.ed2016b.s060100, 
public.ed2016b.s060101,public.ed2016b.s060105, 
public.ed2016b.s060106, public.ed2016b.s060107, 
public.ed2016b.s060111, public.ed2016b.s060800, 
public.ed2016b.s060804
FROM public.ed2016b 
Join public.ed2011b
on   public.ed2016b.ed2016_ed11form=public.ed2011b.ed2011_ed11form 
order by public.ed2011b.ed2011_ed11form asc
LIMIT 10000
