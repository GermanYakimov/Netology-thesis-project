using System;
using System.Collections.Generic;
using System.Net;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace thesis_project
{
    class MainClass
    {
        // apiVersion = "5.8";
        // accessToken = "5da5d12e837aa6bc2f058c6a927e6829eb0545ffedfc840efbc1500567d43271f1d0dc4523515df8c41dd";
        // serverUrl = "https://api.vk.com/method/";

        static int GetIdByShortName(string shortName)
        {
            var accessToken = "5da5d12e837aa6bc2f058c6a927e6829eb0545ffedfc840efbc1500567d43271f1d0dc4523515df8c41dd";
            var serverUrlWithParams = $"https://api.vk.com/method/users.get?access_token={accessToken}&v=5.8&user_ids={shortName}";

            using (var webClient = new WebClient())
            {
                var response = webClient.DownloadString(serverUrlWithParams);
                var result = JsonConvert.DeserializeObject<JToken>(response);
                return Int32.Parse(result["response"][0]["id"].ToString());
            }
        }

        static List<int> GetFriendsId(int id)
        {
            var accessToken = "5da5d12e837aa6bc2f058c6a927e6829eb0545ffedfc840efbc1500567d43271f1d0dc4523515df8c41dd";
            var serverUrlWithParams = $"https://api.vk.com/method/friends.get?access_token={accessToken}&v=5.8&user_ids={id}";

            using (var webClient = new WebClient())
            {
                var friendsIdList = new List<int>();
                var response = webClient.DownloadString(serverUrlWithParams);
                var result = JsonConvert.DeserializeObject<JToken>(response);

                foreach (var item in result["response"]["items"])
                {
                    friendsIdList.Add(Int32.Parse(item.ToString()));
                }

                return friendsIdList;
            }
        }

        static List<int> GetCommunitiesIds(int id)
        {
            var accessToken = "5da5d12e837aa6bc2f058c6a927e6829eb0545ffedfc840efbc1500567d43271f1d0dc4523515df8c41dd";
            var serverUrlWithParams = $"https://api.vk.com/method/groups.get?access_token={accessToken}&v=5.8&user_ids={id}";

            using (var webClient = new WebClient())
            {
                var groupsIdList = new List<int>();
                var response = webClient.DownloadString(serverUrlWithParams);
                var result = JsonConvert.DeserializeObject<JToken>(response);

                foreach (var item in result["response"]["items"])
                {
                    groupsIdList.Add(Int32.Parse(item.ToString()));
                }

                return groupsIdList;
            }
        }

        static List<string> GetCommunitiesNames(int id)
        {
            var accessToken = "5da5d12e837aa6bc2f058c6a927e6829eb0545ffedfc840efbc1500567d43271f1d0dc4523515df8c41dd";
            var serverUrlWithParams = $"https://api.vk.com/method/groups.get?access_token={accessToken}&v=5.8&user_ids={id}&extended=1&fields=name";

            using (var webClient = new WebClient())
            {
                var groupsIdList = new List<string>();
                var response = webClient.DownloadString(serverUrlWithParams);
                var result = JsonConvert.DeserializeObject<JToken>(response);

                foreach (var item in result["response"]["items"])
                {
                    groupsIdList.Add(item["name"].ToString());
                }

                return groupsIdList;
            }
        }

        static Dictionary<int, string> GetCommunitiesInfo(int id)
        {
            var accessToken = "5da5d12e837aa6bc2f058c6a927e6829eb0545ffedfc840efbc1500567d43271f1d0dc4523515df8c41dd";
            var serverUrlWithParams = $"https://api.vk.com/method/groups.get?access_token={accessToken}&v=5.8&user_ids={id}&extended=1&fields=name";

            using (var webClient = new WebClient())
            {
                var groupsDict = new Dictionary<int, string>();
                var response = webClient.DownloadString(serverUrlWithParams);
                var result = JsonConvert.DeserializeObject<JToken>(response);

                foreach (var item in result["response"]["items"])
                {
                    groupsDict.Add(Int32.Parse(item["id"].ToString()), item["name"].ToString());
                }

                return groupsDict;
            }
        }

        public static void Main(string[] args)
        {
            var groupsDict = GetCommunitiesInfo(GetIdByShortName("german_yakimov"));

            foreach (var item in groupsDict)
            {
                Console.WriteLine(item);
            }
        }
    }
}
