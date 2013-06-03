  


<!DOCTYPE html>
<html>
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# githubog: http://ogp.me/ns/fb/githubog#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>scene_labelling_rgbd/pyglpk_setup.py at release2 · hemakoppula/scene_labelling_rgbd · GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png" />
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png" />
    <link rel="logo" type="image/svg" href="http://github-media-downloads.s3.amazonaws.com/github-logo.svg" />
    <link rel="xhr-socket" href="/_sockets" />
    


    <meta name="msapplication-TileImage" content="/windows-tile.png" />
    <meta name="msapplication-TileColor" content="#ffffff" />
    <meta name="selected-link" value="repo_source" data-pjax-transient />
    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="github" name="octolytics-app-id" />

    
    
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />

    <meta content="authenticity_token" name="csrf-param" />
<meta content="sRf8WbU8l3X/CI/j+dfn5WGfX5HqvDohjqp/TymlFfs=" name="csrf-token" />

    <link href="https://a248.e.akamai.net/assets.github.com/assets/github-2e53882cf8306e277ea0d07dbb6117f926c38f6c.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://a248.e.akamai.net/assets.github.com/assets/github2-8ea4ea72d7b478cc437d5b2e6841998ad79f1396.css" media="all" rel="stylesheet" type="text/css" />
    


      <script src="https://a248.e.akamai.net/assets.github.com/assets/frameworks-5c60c478b1e0f90d149f11ed15aa52edd2996882.js" type="text/javascript"></script>
      <script src="https://a248.e.akamai.net/assets.github.com/assets/github-d0435fc89716ef469af722563289b9f1e7c92485.js" type="text/javascript"></script>
      
      <meta http-equiv="x-pjax-version" content="192c0e6b18e09b3349d7b1c470d746d9">

        <link data-pjax-transient rel='permalink' href='/hemakoppula/scene_labelling_rgbd/blob/b370d8adbb499f04dbfd8e63d9731421ced7bdb7/pyglpk_setup.py'>
    <meta property="og:title" content="scene_labelling_rgbd"/>
    <meta property="og:type" content="githubog:gitrepository"/>
    <meta property="og:url" content="https://github.com/hemakoppula/scene_labelling_rgbd"/>
    <meta property="og:image" content="https://secure.gravatar.com/avatar/a143ded0467c92fbfd611bc6e70965bb?s=420&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png"/>
    <meta property="og:site_name" content="GitHub"/>
    <meta property="og:description" content="scene_labelling_rgbd - semantically labels kinect pointclouds"/>
    <meta property="twitter:card" content="summary"/>
    <meta property="twitter:site" content="@GitHub">
    <meta property="twitter:title" content="hemakoppula/scene_labelling_rgbd"/>

    <meta name="description" content="scene_labelling_rgbd - semantically labels kinect pointclouds" />

      <meta name="robots" content="noindex, nofollow">

    <meta content="3735995" name="octolytics-dimension-user_id" /><meta content="hemakoppula" name="octolytics-dimension-user_login" /><meta content="8497380" name="octolytics-dimension-repository_id" /><meta content="hemakoppula/scene_labelling_rgbd" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="true" name="octolytics-dimension-repository_is_fork" /><meta content="2024492" name="octolytics-dimension-repository_parent_id" /><meta content="aa755/scene_labelling_rgbd" name="octolytics-dimension-repository_parent_nwo" /><meta content="2024492" name="octolytics-dimension-repository_network_root_id" /><meta content="aa755/scene_labelling_rgbd" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/hemakoppula/scene_labelling_rgbd/commits/release2.atom" rel="alternate" title="Recent Commits to scene_labelling_rgbd:release2" type="application/atom+xml" />

  </head>


  <body class="logged_out page-blob linux vis-public fork env-production  ">
    <div id="wrapper">

      
      
      

      
      <div class="header header-logged-out">
  <div class="container clearfix">

    <a class="header-logo-wordmark" href="https://github.com/">Github</a>

    <div class="header-actions">
      <a class="button primary" href="/signup">Sign up</a>
      <a class="button" href="/login?return_to=%2Fhemakoppula%2Fscene_labelling_rgbd%2Fblob%2Frelease2%2Fpyglpk_setup.py">Sign in</a>
    </div>

    <div class="command-bar js-command-bar  in-repository">


      <ul class="top-nav">
          <li class="explore"><a href="/explore">Explore</a></li>
        <li class="features"><a href="/features">Features</a></li>
          <li class="enterprise"><a href="http://enterprise.github.com/">Enterprise</a></li>
          <li class="blog"><a href="/blog">Blog</a></li>
      </ul>
        <form accept-charset="UTF-8" action="/search" class="command-bar-form" id="top_search_form" method="get">
  <a href="/search/advanced" class="advanced-search-icon tooltipped downwards command-bar-search" id="advanced_search" title="Advanced search"><span class="octicon octicon-gear "></span></a>

  <input type="text" data-hotkey="/ s" name="q" id="js-command-bar-field" placeholder="Search or type a command" tabindex="1" autocapitalize="off"
    
      data-repo="hemakoppula/scene_labelling_rgbd"
      data-branch="release2"
      data-sha="b1ddf4fa2583100f54bb16ddd4a514ddf6abe804"
  >

    <input type="hidden" name="nwo" value="hemakoppula/scene_labelling_rgbd" />

    <div class="select-menu js-menu-container js-select-menu search-context-select-menu">
      <span class="minibutton select-menu-button js-menu-target">
        <span class="js-select-button">This repository</span>
      </span>

      <div class="select-menu-modal-holder js-menu-content js-navigation-container">
        <div class="select-menu-modal">

          <div class="select-menu-item js-navigation-item selected">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" class="js-search-this-repository" name="search_target" value="repository" checked="checked" />
            <div class="select-menu-item-text js-select-button-text">This repository</div>
          </div> <!-- /.select-menu-item -->

          <div class="select-menu-item js-navigation-item">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" name="search_target" value="global" />
            <div class="select-menu-item-text js-select-button-text">All repositories</div>
          </div> <!-- /.select-menu-item -->

        </div>
      </div>
    </div>

  <span class="octicon help tooltipped downwards" title="Show command bar help">
    <span class="octicon octicon-question"></span>
  </span>


  <input type="hidden" name="ref" value="cmdform">

  <div class="divider-vertical"></div>

</form>
    </div>

  </div>
</div>


      


            <div class="site hfeed" itemscope itemtype="http://schema.org/WebPage">
      <div class="hentry">
        
        <div class="pagehead repohead instapaper_ignore readability-menu ">
          <div class="container">
            <div class="title-actions-bar">
              

<ul class="pagehead-actions">



    <li>
      <a href="/login?return_to=%2Fhemakoppula%2Fscene_labelling_rgbd"
        class="minibutton js-toggler-target star-button entice tooltipped upwards"
        title="You must be signed in to use this feature" rel="nofollow">
        <span class="octicon octicon-star"></span>Star
      </a>
      <a class="social-count js-social-count" href="/hemakoppula/scene_labelling_rgbd/stargazers">
        0
      </a>
    </li>
    <li>
      <a href="/login?return_to=%2Fhemakoppula%2Fscene_labelling_rgbd"
        class="minibutton js-toggler-target fork-button entice tooltipped upwards"
        title="You must be signed in to fork a repository" rel="nofollow">
        <span class="octicon octicon-git-branch"></span>Fork
      </a>
      <a href="/hemakoppula/scene_labelling_rgbd/network" class="social-count">
        7
      </a>
    </li>
</ul>

              <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
                <span class="repo-label"><span>public</span></span>
                <span class="mega-octicon octicon-repo"></span>
                <span class="author vcard">
                  <a href="/hemakoppula" class="url fn" itemprop="url" rel="author">
                  <span itemprop="title">hemakoppula</span>
                  </a></span> /
                <strong><a href="/hemakoppula/scene_labelling_rgbd" class="js-current-repository">scene_labelling_rgbd</a></strong>
                  <span class="fork-flag">
                    <span class="text">forked from <a href="/aa755/scene_labelling_rgbd">aa755/scene_labelling_rgbd</a></span>
                  </span>
              </h1>
            </div>

            
  <ul class="tabs">
    <li class="pulse-nav"><a href="/hemakoppula/scene_labelling_rgbd/pulse" class="js-selected-navigation-item " data-selected-links="pulse /hemakoppula/scene_labelling_rgbd/pulse" rel="nofollow"><span class="octicon octicon-pulse"></span></a></li>
    <li><a href="/hemakoppula/scene_labelling_rgbd" class="js-selected-navigation-item selected" data-selected-links="repo_source repo_downloads repo_commits repo_tags repo_branches /hemakoppula/scene_labelling_rgbd">Code</a></li>
    <li><a href="/hemakoppula/scene_labelling_rgbd/network" class="js-selected-navigation-item " data-selected-links="repo_network /hemakoppula/scene_labelling_rgbd/network">Network</a></li>
    <li><a href="/hemakoppula/scene_labelling_rgbd/pulls" class="js-selected-navigation-item " data-selected-links="repo_pulls /hemakoppula/scene_labelling_rgbd/pulls">Pull Requests <span class='counter'>0</span></a></li>




    <li><a href="/hemakoppula/scene_labelling_rgbd/graphs" class="js-selected-navigation-item " data-selected-links="repo_graphs repo_contributors /hemakoppula/scene_labelling_rgbd/graphs">Graphs</a></li>


  </ul>
  
<div class="tabnav">

  <span class="tabnav-right">
    <ul class="tabnav-tabs">
          <li><a href="/hemakoppula/scene_labelling_rgbd/tags" class="js-selected-navigation-item tabnav-tab" data-selected-links="repo_tags /hemakoppula/scene_labelling_rgbd/tags">Tags <span class="counter blank">0</span></a></li>
    </ul>
  </span>

  <div class="tabnav-widget scope">


    <div class="select-menu js-menu-container js-select-menu js-branch-menu">
      <a class="minibutton select-menu-button js-menu-target" data-hotkey="w" data-ref="release2">
        <span class="octicon octicon-branch"></span>
        <i>branch:</i>
        <span class="js-select-button">release2</span>
      </a>

      <div class="select-menu-modal-holder js-menu-content js-navigation-container">

        <div class="select-menu-modal">
          <div class="select-menu-header">
            <span class="select-menu-title">Switch branches/tags</span>
            <span class="octicon octicon-remove-close js-menu-close"></span>
          </div> <!-- /.select-menu-header -->

          <div class="select-menu-filters">
            <div class="select-menu-text-filter">
              <input type="text" id="commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
            </div>
            <div class="select-menu-tabs">
              <ul>
                <li class="select-menu-tab">
                  <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
                </li>
                <li class="select-menu-tab">
                  <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
                </li>
              </ul>
            </div><!-- /.select-menu-tabs -->
          </div><!-- /.select-menu-filters -->

          <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket css-truncate" data-tab-filter="branches">

            <div data-filterable-for="commitish-filter-field" data-filterable-type="substring">

                <div class="select-menu-item js-navigation-item selected">
                  <span class="select-menu-item-icon octicon octicon-check"></span>
                  <a href="/hemakoppula/scene_labelling_rgbd/blob/release2/pyglpk_setup.py" class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target" data-name="release2" rel="nofollow" title="release2">release2</a>
                </div> <!-- /.select-menu-item -->
            </div>

              <div class="select-menu-no-results">Nothing to show</div>
          </div> <!-- /.select-menu-list -->


          <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket css-truncate" data-tab-filter="tags">
            <div data-filterable-for="commitish-filter-field" data-filterable-type="substring">

            </div>

            <div class="select-menu-no-results">Nothing to show</div>

          </div> <!-- /.select-menu-list -->

        </div> <!-- /.select-menu-modal -->
      </div> <!-- /.select-menu-modal-holder -->
    </div> <!-- /.select-menu -->

  </div> <!-- /.scope -->

  <ul class="tabnav-tabs">
    <li><a href="/hemakoppula/scene_labelling_rgbd" class="selected js-selected-navigation-item tabnav-tab" data-selected-links="repo_source /hemakoppula/scene_labelling_rgbd">Files</a></li>
    <li><a href="/hemakoppula/scene_labelling_rgbd/commits/release2" class="js-selected-navigation-item tabnav-tab" data-selected-links="repo_commits /hemakoppula/scene_labelling_rgbd/commits/release2">Commits</a></li>
    <li><a href="/hemakoppula/scene_labelling_rgbd/branches" class="js-selected-navigation-item tabnav-tab" data-selected-links="repo_branches /hemakoppula/scene_labelling_rgbd/branches" rel="nofollow">Branches <span class="counter ">1</span></a></li>
  </ul>

</div>

  
  
  


            
          </div>
        </div><!-- /.repohead -->

        <div id="js-repo-pjax-container" class="container context-loader-container" data-pjax-container>
          


<!-- blob contrib key: blob_contributors:v21:c205e27ea9be88ddeb86c2156771d715 -->
<!-- blob contrib frag key: views10/v8/blob_contributors:v21:c205e27ea9be88ddeb86c2156771d715 -->


<div id="slider">
    <div class="frame-meta">

      <p title="This is a placeholder element" class="js-history-link-replace hidden"></p>

        <div class="breadcrumb">
          <span class='bold'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/hemakoppula/scene_labelling_rgbd" class="js-slide-to" data-branch="release2" data-direction="back" itemscope="url"><span itemprop="title">scene_labelling_rgbd</span></a></span></span><span class="separator"> / </span><strong class="final-path">pyglpk_setup.py</strong> <span class="js-zeroclipboard zeroclipboard-button" data-clipboard-text="pyglpk_setup.py" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
        </div>

      <a href="/hemakoppula/scene_labelling_rgbd/find/release2" class="js-slide-to" data-hotkey="t" style="display:none">Show File Finder</a>


        
  <div class="commit file-history-tease">
    <img class="main-avatar" height="24" src="https://secure.gravatar.com/avatar/dbef449fe7316c765afeed5d8a28885a?s=140&amp;d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-user-420.png" width="24" />
    <span class="author"><span rel="author">nav</span></span>
    <time class="js-relative-date" datetime="2011-06-22T17:27:20-07:00" title="2011-06-22 17:27:20">June 22, 2011</time>
    <div class="commit-title">
        <a href="/hemakoppula/scene_labelling_rgbd/commit/eb03d982b890ad1a63834222e92407e6ef1c3a44" class="message"> setup file for 64 bit machines</a>
    </div>

    <div class="participation">
      <p class="quickstat"><a href="#blob_contributors_box" rel="facebox"><strong>0</strong> contributors</a></p>
      
    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
      </ul>
    </div>
  </div>


    </div><!-- ./.frame-meta -->

    <div class="frames">
      <div class="frame" data-permalink-url="/hemakoppula/scene_labelling_rgbd/blob/b370d8adbb499f04dbfd8e63d9731421ced7bdb7/pyglpk_setup.py" data-title="scene_labelling_rgbd/pyglpk_setup.py at release2 · hemakoppula/scene_labelling_rgbd · GitHub" data-type="blob">

        <div id="files" class="bubble">
          <div class="file">
            <div class="meta">
              <div class="info">
                <span class="icon"><b class="octicon octicon-file-text"></b></span>
                <span class="mode" title="File Mode">file</span>
                  <span>101 lines (86 sloc)</span>
                <span>3.572 kb</span>
              </div>
              <div class="actions">
                <div class="button-group">
                      <a class="minibutton js-entice" href=""
                         data-entice="You must be signed in and on a branch to make or propose changes">Edit</a>
                  <a href="/hemakoppula/scene_labelling_rgbd/raw/release2/pyglpk_setup.py" class="button minibutton " id="raw-url">Raw</a>
                    <a href="/hemakoppula/scene_labelling_rgbd/blame/release2/pyglpk_setup.py" class="button minibutton ">Blame</a>
                  <a href="/hemakoppula/scene_labelling_rgbd/commits/release2/pyglpk_setup.py" class="button minibutton " rel="nofollow">History</a>
                </div><!-- /.button-group -->
              </div><!-- /.actions -->

            </div>
                <div class="blob-wrapper data type-python js-blob-data">
      <table class="file-code file-diff">
        <tr class="file-code-line">
          <td class="blob-line-nums">
            <span id="L1" rel="#L1">1</span>
<span id="L2" rel="#L2">2</span>
<span id="L3" rel="#L3">3</span>
<span id="L4" rel="#L4">4</span>
<span id="L5" rel="#L5">5</span>
<span id="L6" rel="#L6">6</span>
<span id="L7" rel="#L7">7</span>
<span id="L8" rel="#L8">8</span>
<span id="L9" rel="#L9">9</span>
<span id="L10" rel="#L10">10</span>
<span id="L11" rel="#L11">11</span>
<span id="L12" rel="#L12">12</span>
<span id="L13" rel="#L13">13</span>
<span id="L14" rel="#L14">14</span>
<span id="L15" rel="#L15">15</span>
<span id="L16" rel="#L16">16</span>
<span id="L17" rel="#L17">17</span>
<span id="L18" rel="#L18">18</span>
<span id="L19" rel="#L19">19</span>
<span id="L20" rel="#L20">20</span>
<span id="L21" rel="#L21">21</span>
<span id="L22" rel="#L22">22</span>
<span id="L23" rel="#L23">23</span>
<span id="L24" rel="#L24">24</span>
<span id="L25" rel="#L25">25</span>
<span id="L26" rel="#L26">26</span>
<span id="L27" rel="#L27">27</span>
<span id="L28" rel="#L28">28</span>
<span id="L29" rel="#L29">29</span>
<span id="L30" rel="#L30">30</span>
<span id="L31" rel="#L31">31</span>
<span id="L32" rel="#L32">32</span>
<span id="L33" rel="#L33">33</span>
<span id="L34" rel="#L34">34</span>
<span id="L35" rel="#L35">35</span>
<span id="L36" rel="#L36">36</span>
<span id="L37" rel="#L37">37</span>
<span id="L38" rel="#L38">38</span>
<span id="L39" rel="#L39">39</span>
<span id="L40" rel="#L40">40</span>
<span id="L41" rel="#L41">41</span>
<span id="L42" rel="#L42">42</span>
<span id="L43" rel="#L43">43</span>
<span id="L44" rel="#L44">44</span>
<span id="L45" rel="#L45">45</span>
<span id="L46" rel="#L46">46</span>
<span id="L47" rel="#L47">47</span>
<span id="L48" rel="#L48">48</span>
<span id="L49" rel="#L49">49</span>
<span id="L50" rel="#L50">50</span>
<span id="L51" rel="#L51">51</span>
<span id="L52" rel="#L52">52</span>
<span id="L53" rel="#L53">53</span>
<span id="L54" rel="#L54">54</span>
<span id="L55" rel="#L55">55</span>
<span id="L56" rel="#L56">56</span>
<span id="L57" rel="#L57">57</span>
<span id="L58" rel="#L58">58</span>
<span id="L59" rel="#L59">59</span>
<span id="L60" rel="#L60">60</span>
<span id="L61" rel="#L61">61</span>
<span id="L62" rel="#L62">62</span>
<span id="L63" rel="#L63">63</span>
<span id="L64" rel="#L64">64</span>
<span id="L65" rel="#L65">65</span>
<span id="L66" rel="#L66">66</span>
<span id="L67" rel="#L67">67</span>
<span id="L68" rel="#L68">68</span>
<span id="L69" rel="#L69">69</span>
<span id="L70" rel="#L70">70</span>
<span id="L71" rel="#L71">71</span>
<span id="L72" rel="#L72">72</span>
<span id="L73" rel="#L73">73</span>
<span id="L74" rel="#L74">74</span>
<span id="L75" rel="#L75">75</span>
<span id="L76" rel="#L76">76</span>
<span id="L77" rel="#L77">77</span>
<span id="L78" rel="#L78">78</span>
<span id="L79" rel="#L79">79</span>
<span id="L80" rel="#L80">80</span>
<span id="L81" rel="#L81">81</span>
<span id="L82" rel="#L82">82</span>
<span id="L83" rel="#L83">83</span>
<span id="L84" rel="#L84">84</span>
<span id="L85" rel="#L85">85</span>
<span id="L86" rel="#L86">86</span>
<span id="L87" rel="#L87">87</span>
<span id="L88" rel="#L88">88</span>
<span id="L89" rel="#L89">89</span>
<span id="L90" rel="#L90">90</span>
<span id="L91" rel="#L91">91</span>
<span id="L92" rel="#L92">92</span>
<span id="L93" rel="#L93">93</span>
<span id="L94" rel="#L94">94</span>
<span id="L95" rel="#L95">95</span>
<span id="L96" rel="#L96">96</span>
<span id="L97" rel="#L97">97</span>
<span id="L98" rel="#L98">98</span>
<span id="L99" rel="#L99">99</span>
<span id="L100" rel="#L100">100</span>

          </td>
          <td class="blob-line-code">
                  <div class="highlight"><pre><div class='line' id='LC1'><span class="kn">from</span> <span class="nn">distutils.core</span> <span class="kn">import</span> <span class="n">setup</span><span class="p">,</span> <span class="n">Extension</span></div><div class='line' id='LC2'><span class="kn">import</span> <span class="nn">sys</span><span class="o">,</span> <span class="nn">os</span><span class="o">,</span> <span class="nn">os.path</span><span class="o">,</span> <span class="nn">re</span></div><div class='line' id='LC3'><br/></div><div class='line' id='LC4'><span class="n">useparams</span> <span class="o">=</span> <span class="bp">False</span></div><div class='line' id='LC5'><br/></div><div class='line' id='LC6'><span class="n">sources</span> <span class="o">=</span> <span class="s">&#39;glpk lp barcol bar obj util kkt tree environment&#39;</span></div><div class='line' id='LC7'><span class="n">source_roots</span> <span class="o">=</span> <span class="n">sources</span><span class="o">.</span><span class="n">split</span><span class="p">()</span></div><div class='line' id='LC8'><span class="k">if</span> <span class="n">useparams</span><span class="p">:</span> <span class="n">source_roots</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="s">&#39;params&#39;</span><span class="p">)</span></div><div class='line' id='LC9'><br/></div><div class='line' id='LC10'><span class="c"># This build process will not work with anything prior to GLPK 4.16,</span></div><div class='line' id='LC11'><span class="c"># since there were many notable changes in GLPK including,</span></div><div class='line' id='LC12'><span class="c"># importantly, something which actually contains the version number.</span></div><div class='line' id='LC13'><br/></div><div class='line' id='LC14'><span class="n">libdirs</span><span class="p">,</span> <span class="n">incdirs</span><span class="p">,</span> <span class="n">extraobs</span> <span class="o">=</span> <span class="p">[],</span> <span class="p">[],</span> <span class="p">[]</span></div><div class='line' id='LC15'><br/></div><div class='line' id='LC16'><span class="c"># The glpver argument is one which is used only for the purposes of</span></div><div class='line' id='LC17'><span class="c"># PyGLPK development, and will be of no use or interest to the</span></div><div class='line' id='LC18'><span class="c"># standard practitioner.  In order to assure compatibility with the</span></div><div class='line' id='LC19'><span class="c"># many GLPK versions which exist, it is helpful to build against one</span></div><div class='line' id='LC20'><span class="c"># of many</span></div><div class='line' id='LC21'><br/></div><div class='line' id='LC22'><span class="c"># This is very dirty.</span></div><div class='line' id='LC23'><span class="n">m</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="s">&#39;glpver=(\d+)&#39;</span><span class="p">,</span> <span class="n">sys</span><span class="o">.</span><span class="n">argv</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">])</span></div><div class='line' id='LC24'><span class="k">if</span> <span class="n">m</span><span class="p">:</span></div><div class='line' id='LC25'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># We have defined that we want to build to a local GLPK version.</span></div><div class='line' id='LC26'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">minor_version</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="n">m</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">1</span><span class="p">))</span></div><div class='line' id='LC27'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">assert</span> <span class="n">minor_version</span> <span class="o">&gt;=</span> <span class="mi">16</span></div><div class='line' id='LC28'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sys</span><span class="o">.</span><span class="n">argv</span> <span class="o">=</span> <span class="n">sys</span><span class="o">.</span><span class="n">argv</span><span class="p">[:</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span></div><div class='line' id='LC29'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">libdirs</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="s">&#39;locals&#39;</span><span class="p">,</span> <span class="s">&#39;4.</span><span class="si">%d</span><span class="s">&#39;</span><span class="o">%</span><span class="n">minor_version</span><span class="p">,</span> <span class="s">&#39;lib&#39;</span><span class="p">))</span></div><div class='line' id='LC30'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">incdirs</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="s">&#39;locals&#39;</span><span class="p">,</span> <span class="s">&#39;4.</span><span class="si">%d</span><span class="s">&#39;</span><span class="o">%</span><span class="n">minor_version</span><span class="p">,</span> <span class="s">&#39;include&#39;</span><span class="p">))</span></div><div class='line' id='LC31'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">minor_version</span><span class="o">&lt;</span><span class="mi">37</span><span class="p">:</span></div><div class='line' id='LC32'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">libs</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;glpk.0.</span><span class="si">%d</span><span class="s">.0&#39;</span><span class="o">%</span><span class="p">(</span><span class="n">minor_version</span><span class="o">-</span><span class="mi">15</span><span class="p">)]</span></div><div class='line' id='LC33'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">else</span><span class="p">:</span></div><div class='line' id='LC34'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">libs</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;glpk.0&#39;</span><span class="p">]</span></div><div class='line' id='LC35'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">print</span> <span class="p">(</span><span class="n">libdirs</span><span class="p">,</span> <span class="n">incdirs</span><span class="p">)</span></div><div class='line' id='LC36'><span class="k">else</span><span class="p">:</span></div><div class='line' id='LC37'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># Try to get which is the executable path, and infer additional</span></div><div class='line' id='LC38'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># library and include directories from there, based on a call to</span></div><div class='line' id='LC39'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># whatever glpsol we find.</span></div><div class='line' id='LC40'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">glpsol_path</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">popen</span><span class="p">(</span><span class="s">&#39;which glpsol&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">read</span><span class="p">()</span><span class="o">.</span><span class="n">strip</span><span class="p">()</span></div><div class='line' id='LC41'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># If we can&#39;t find it, just hope that the default libs are correct.</span></div><div class='line' id='LC42'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">glpsol_path</span><span class="p">:</span></div><div class='line' id='LC43'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">glpsol_path</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">abspath</span><span class="p">(</span><span class="n">glpsol_path</span><span class="p">)</span></div><div class='line' id='LC44'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">head</span><span class="p">,</span> <span class="n">tail</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="n">glpsol_path</span><span class="p">)</span></div><div class='line' id='LC45'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">head</span><span class="p">,</span> <span class="n">tail</span> <span class="o">=</span> <span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="n">head</span><span class="p">)</span></div><div class='line' id='LC46'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">libdirs</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">head</span><span class="p">,</span> <span class="s">&#39;lib&#39;</span><span class="p">))</span></div><div class='line' id='LC47'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">incdirs</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">head</span><span class="p">,</span> <span class="s">&#39;include&#39;</span><span class="p">))</span></div><div class='line' id='LC48'><br/></div><div class='line' id='LC49'><span class="c"># USERS DO CUSTOM INSTRUCTIONS HERE</span></div><div class='line' id='LC50'><span class="c"># Perhaps set your libdir manually in case neither system defaults,</span></div><div class='line' id='LC51'><span class="c"># nor the cleverness does not work.</span></div><div class='line' id='LC52'><br/></div><div class='line' id='LC53'><span class="c">#libs = [&#39;glpk.something&#39;]</span></div><div class='line' id='LC54'><span class="c">#libdirs = [&#39;/my/dirs/are/here/lib&#39;]</span></div><div class='line' id='LC55'><span class="c">#incdirs = [&#39;/my/dirs/are/here/include&#39;]</span></div><div class='line' id='LC56'><br/></div><div class='line' id='LC57'><span class="c"># If the user did not define libraries themselves, set that up.  We</span></div><div class='line' id='LC58'><span class="c"># require both glpk and gmp.</span></div><div class='line' id='LC59'><span class="k">try</span><span class="p">:</span></div><div class='line' id='LC60'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">libs</span></div><div class='line' id='LC61'><span class="k">except</span> <span class="ne">NameError</span><span class="p">:</span></div><div class='line' id='LC62'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># The user nor test code did not set libs up yet.</span></div><div class='line' id='LC63'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">libs</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;glpk&#39;</span><span class="p">,</span> <span class="s">&#39;gmp&#39;</span><span class="p">]</span></div><div class='line' id='LC64'><br/></div><div class='line' id='LC65'><span class="n">incdirs</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="s">&#39;src&#39;</span><span class="p">)</span></div><div class='line' id='LC66'><br/></div><div class='line' id='LC67'><span class="n">macros</span> <span class="o">=</span> <span class="p">[]</span></div><div class='line' id='LC68'><span class="k">if</span> <span class="n">useparams</span><span class="p">:</span> <span class="n">macros</span><span class="o">.</span><span class="n">append</span><span class="p">((</span><span class="s">&#39;USEPARAMS&#39;</span><span class="p">,</span> <span class="bp">None</span><span class="p">))</span></div><div class='line' id='LC69'><br/></div><div class='line' id='LC70'><span class="c"># Now, finally, define that module!</span></div><div class='line' id='LC71'><span class="n">module1</span> <span class="o">=</span> <span class="n">Extension</span><span class="p">(</span></div><div class='line' id='LC72'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;glpk&#39;</span><span class="p">,</span></div><div class='line' id='LC73'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">sources</span> <span class="o">=</span> <span class="p">[</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="s">&#39;src&#39;</span><span class="p">,</span><span class="n">r</span><span class="o">+</span><span class="s">&#39;.c&#39;</span><span class="p">)</span> <span class="k">for</span> <span class="n">r</span> <span class="ow">in</span> <span class="n">source_roots</span><span class="p">],</span></div><div class='line' id='LC74'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">define_macros</span> <span class="o">=</span> <span class="n">macros</span><span class="p">,</span> <span class="n">extra_compile_args</span><span class="o">=</span><span class="p">[</span><span class="s">&#39;-m64&#39;</span><span class="p">],</span> <span class="n">extra_link_args</span><span class="o">=</span><span class="p">[</span><span class="s">&#39;-m64&#39;</span><span class="p">],</span></div><div class='line' id='LC75'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">library_dirs</span> <span class="o">=</span> <span class="n">libdirs</span><span class="p">,</span> <span class="n">include_dirs</span> <span class="o">=</span> <span class="n">incdirs</span><span class="p">,</span></div><div class='line' id='LC76'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">libraries</span> <span class="o">=</span> <span class="n">libs</span><span class="p">,</span> <span class="n">extra_objects</span> <span class="o">=</span> <span class="n">extraobs</span><span class="p">)</span></div><div class='line' id='LC77'><br/></div><div class='line' id='LC78'><span class="n">ld</span> <span class="o">=</span> <span class="s">&quot;&quot;&quot;The PyGLPK module gives one access to the functionality</span></div><div class='line' id='LC79'><span class="s">of the GNU Linear Programming Kit.  </span></div><div class='line' id='LC80'><span class="s">&quot;&quot;&quot;</span></div><div class='line' id='LC81'><br/></div><div class='line' id='LC82'><span class="n">setup</span><span class="p">(</span><span class="n">name</span> <span class="o">=</span> <span class="s">&#39;glpk&#39;</span><span class="p">,</span></div><div class='line' id='LC83'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">version</span> <span class="o">=</span> <span class="s">&#39;0.3&#39;</span><span class="p">,</span></div><div class='line' id='LC84'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">description</span> <span class="o">=</span> <span class="s">&#39;PyGLPK, a Python module encapsulating GLPK.&#39;</span><span class="p">,</span></div><div class='line' id='LC85'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">long_description</span> <span class="o">=</span> <span class="n">ld</span><span class="p">,</span></div><div class='line' id='LC86'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">author</span> <span class="o">=</span> <span class="s">&#39;Thomas Finley&#39;</span><span class="p">,</span></div><div class='line' id='LC87'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">author_email</span> <span class="o">=</span> <span class="s">&#39;tfinley@gmail.com&#39;</span><span class="p">,</span></div><div class='line' id='LC88'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">url</span> <span class="o">=</span> <span class="s">&#39;http://tfinley.net/software/pyglpk/&#39;</span><span class="p">,</span></div><div class='line' id='LC89'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">license</span> <span class="o">=</span> <span class="s">&#39;GPL&#39;</span><span class="p">,</span></div><div class='line' id='LC90'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">classifiers</span> <span class="o">=</span> <span class="p">[</span></div><div class='line' id='LC91'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Development Status :: 3 - Alpha&#39;</span><span class="p">,</span></div><div class='line' id='LC92'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Intended Audience :: Science/Research&#39;</span><span class="p">,</span></div><div class='line' id='LC93'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;License :: OSI Approved :: GNU General Public License (GPL)&#39;</span><span class="p">,</span></div><div class='line' id='LC94'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Programming Language :: C&#39;</span><span class="p">,</span></div><div class='line' id='LC95'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Programming Language :: Python&#39;</span><span class="p">,</span></div><div class='line' id='LC96'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Operating System :: POSIX&#39;</span><span class="p">,</span></div><div class='line' id='LC97'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Operating System :: MacOS :: MacOS X&#39;</span><span class="p">,</span></div><div class='line' id='LC98'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Topic :: Scientific/Engineering :: Mathematics&#39;</span><span class="p">,</span></div><div class='line' id='LC99'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="s">&#39;Topic :: Software Development :: Libraries :: Python Modules&#39;</span> <span class="p">],</span></div><div class='line' id='LC100'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ext_modules</span> <span class="o">=</span> <span class="p">[</span><span class="n">module1</span><span class="p">])</span></div></pre></div>
          </td>
        </tr>
      </table>
  </div>

          </div>
        </div>

        <a href="#jump-to-line" rel="facebox" data-hotkey="l" class="js-jump-to-line" style="display:none">Jump to Line</a>
        <div id="jump-to-line" style="display:none">
          <h2>Jump to Line</h2>
          <form accept-charset="UTF-8" class="js-jump-to-line-form">
            <input class="textfield js-jump-to-line-field" type="text">
            <div class="full-button">
              <button type="submit" class="button">Go</button>
            </div>
          </form>
        </div>

      </div>
    </div>
</div>

<div id="js-frame-loading-template" class="frame frame-loading large-loading-area" style="display:none;">
  <img class="js-frame-loading-spinner" src="https://a248.e.akamai.net/assets.github.com/images/spinners/octocat-spinner-128.gif?1347543529" height="64" width="64">
</div>


        </div>
      </div>
      <div class="modal-backdrop"></div>
    </div>

      <div id="footer-push"></div><!-- hack for sticky footer -->
    </div><!-- end of wrapper - hack for sticky footer -->

      <!-- footer -->
      <div id="footer">
  <div class="container clearfix">

      <dl class="footer_nav">
        <dt>GitHub</dt>
        <dd><a href="/about">About us</a></dd>
        <dd><a href="/blog">Blog</a></dd>
        <dd><a href="/contact">Contact &amp; support</a></dd>
        <dd><a href="http://enterprise.github.com/">GitHub Enterprise</a></dd>
        <dd><a href="http://status.github.com/">Site status</a></dd>
      </dl>

      <dl class="footer_nav">
        <dt>Applications</dt>
        <dd><a href="http://mac.github.com/">GitHub for Mac</a></dd>
        <dd><a href="http://windows.github.com/">GitHub for Windows</a></dd>
        <dd><a href="http://eclipse.github.com/">GitHub for Eclipse</a></dd>
        <dd><a href="http://mobile.github.com/">GitHub mobile apps</a></dd>
      </dl>

      <dl class="footer_nav">
        <dt>Services</dt>
        <dd><a href="http://get.gaug.es/">Gauges: Web analytics</a></dd>
        <dd><a href="http://speakerdeck.com">Speaker Deck: Presentations</a></dd>
        <dd><a href="https://gist.github.com">Gist: Code snippets</a></dd>
        <dd><a href="http://jobs.github.com/">Job board</a></dd>
      </dl>

      <dl class="footer_nav">
        <dt>Documentation</dt>
        <dd><a href="http://help.github.com/">GitHub Help</a></dd>
        <dd><a href="http://developer.github.com/">Developer API</a></dd>
        <dd><a href="http://github.github.com/github-flavored-markdown/">GitHub Flavored Markdown</a></dd>
        <dd><a href="http://pages.github.com/">GitHub Pages</a></dd>
      </dl>

      <dl class="footer_nav">
        <dt>More</dt>
        <dd><a href="http://training.github.com/">Training</a></dd>
        <dd><a href="/edu">Students &amp; teachers</a></dd>
        <dd><a href="http://shop.github.com">The Shop</a></dd>
        <dd><a href="/plans">Plans &amp; pricing</a></dd>
        <dd><a href="http://octodex.github.com/">The Octodex</a></dd>
      </dl>

      <hr class="footer-divider">


    <p class="right">&copy; 2013 <span title="0.04710s from fe13.rs.github.com">GitHub</span>, Inc. All rights reserved.</p>
    <a class="left" href="/">
      <span class="mega-octicon octicon-mark-github"></span>
    </a>
    <ul id="legal">
        <li><a href="/site/terms">Terms of Service</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
    </ul>

  </div><!-- /.container -->

</div><!-- /.#footer -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-fullscreen-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="js-fullscreen-contents" placeholder="" data-suggester="fullscreen_suggester"></textarea>
          <div class="suggester-container">
              <div class="suggester fullscreen-suggester js-navigation-container" id="fullscreen_suggester"
                 data-url="/hemakoppula/scene_labelling_rgbd/suggestions/commit">
              </div>
          </div>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped leftwards" title="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped leftwards"
      title="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      Something went wrong with that request. Please try again.
      <a href="#" class="octicon octicon-remove-close ajax-error-dismiss"></a>
    </div>

    
    <span id='server_response_time' data-time='0.04750' data-host='fe13'></span>
    
  </body>
</html>

