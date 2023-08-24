class Solution {
public:
    bool isAnagram(string s, string t) {
        if(s.length()==t.length()){
            sort(s.begin(), s.end());
            cout<<s;
            sort(t.begin(), t.end());
            if(s == t){
                return true;
            }
            else{
                return false;
            }
        }
        else{
            return false;
        }
    }
};
