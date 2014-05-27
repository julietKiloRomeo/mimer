function put(map, hashtable, filename)

N = numel(map.T);
for i=1:N
    key         = num2str( round(map.f(i)) );
    val.name    = filename;
    val.T       = map.T(i);
    
    if isKey(hashtable,key)
        oldval          = hashtable(key);
        already_in_db   = false;
        for i=1:numel(oldval)
            already_in_db  = already_in_db || strcmp(oldval(i).name, val.name) && val.T==oldval(i).T;
        end
        if ~already_in_db
            oldval(end+1)   = val;
            hashtable(key)  = oldval;
        end
    else
        hashtable(key)  = val;
    end
end